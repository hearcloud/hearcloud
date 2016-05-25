#! -*- codin: utf-8 -*-

from __future__ import unicode_literals

import uuid
import mimetypes
import datetime
import os

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
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

from .functions import (mp3_tags_to_song_model, tags_from_song_model_to_mp3,
                      m4a_tags_to_song_model)

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

    def save(self, create= False, update=False, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.song_title)

        if create:
            file_final_path = self.audio_file.path
            file_name = self.audio_file.name
            file_type = file_final_path.split('.')[-1].lower()
            file_temp_path = os.path.join(settings.MEDIA_ROOT,'tmp','temp.'+file_type)
            default_storage.save(file_temp_path,ContentFile(self.audio_file.file.read()))

            # MP3
            if file_type == "mp3":
                mp3_tags_to_song_model(file_name, file_temp_path, self)

            # MP4
            elif file_type == "m4a":
                m4a_tags_to_song_model(file_name, file_temp_path, self)

            default_storage.delete(os.path.join(settings.MEDIA_ROOT,'tmp','temp.'+file_type))
        
            # If there is no 'Title' attribute, use the filename as title
            if not self.song_title:
                self.song_title = os.path.splitext(file_name)[0]
        elif update:
            tags_from_song_model_to_mp3(self)


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
