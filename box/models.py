#! -*- codin: utf-8 -*-

from __future__ import unicode_literals

import uuid
import mimetypes
import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete # Receive the pre_delete signal and delete the file associated with the model instance.
from django.dispatch.dispatcher import receiver
from django.db import models

from django.conf import settings

class Song(models.Model):
    """
    Song model
    """
    #: Universally unique identifier
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False)

    #: Creation time
    ctime = models.DateField(auto_now_add=True)

    #: Modified time
    mtime = models.DateField(auto_now=True)

    #: User which this song file belongs to
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    # Slug
    slug = models.SlugField()

    #: Song file itself
    audio_file = models.FileField(default='')

    #: File mime type
    mime_type = models.CharField(_('Mime type'), blank=True, max_length=256)

    # Attached picture/cover/logo/artwork
    artwork = models.ImageField(blank=True, null=True)

    #: The song's title
    song_title = models.CharField(max_length=250, blank=True, null=True)

    #: Artist (lead performer(s)/soloist(s)
    artist = models.CharField(max_length=250, blank=True, null=True) 

    #: Releasing year
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(3000)],
        blank=True, 
        null=True
    ) 

    #: Album which the song belongs to
    album = models.CharField(max_length=500, blank=True, null=True) 

    #: Complete release date (day-month-year)
    release_date = models.DateField(blank=True, null=True) 
    
    #: Album artist: band/orchestra/accompaniment
    album_artist = models.CharField(max_length=250, blank=True, null=True)

    #: Track number: position in set
    track_number = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(3000)],
        blank=True, 
        null=True
    )

    #: Beats per minute
    bpm = models.FloatField(
        validators=[MinValueValidator(5), MaxValueValidator(300)],
        blank=True, 
        null=True
    )
    
    #: Original artist(s)/performer(s)
    original_artist = models.CharField(max_length=250, blank=True, null=True) 

    #: Key which the track is written
    key = models.CharField(max_length=50, blank=True, null=True)

    #: Composer
    composer = models.CharField(max_length=250, blank=True, null=True)

    #: Lyricist/text writer
    lyricist = models.CharField(max_length=250, blank=True, null=True)

    #: Comments
    comments = models.CharField(max_length=500, blank=True, null=True)

    #: Interpreted, remixed or otherwise modified by 
    remixer = models.CharField(max_length=250, blank=True, null=True)

    #: Label/Publisher
    label = models.CharField(max_length=250, blank=True, null=True)

    #: Genre/content type
    genre = models.CharField(max_length=100, blank=True, null=True)

    #: Duration
    duration = models.DurationField(blank=True, null=True)
    
    #: Where to be redirected after you add a new song
    def get_absolute_url(self):
        return reverse('box:detail-update', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.song_title)
        super(Song, self).save(*args, **kwargs)
            
    def __unicode__(self):
        return self.audio_file.name

@receiver(pre_delete, sender=Song)
def song_delete(sender, instance, **kwargs):
    """
    Things to do before delete a song field from the db
    """
    # Pass false so FileField doesn't save the model.
    instance.audio_file.delete(False)
    instance.artwork.delete(False)
