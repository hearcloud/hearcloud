#! -*- codin: utf-8 -*-

from __future__ import unicode_literals

import uuid
import mimetypes
import datetime
import os
import humanize

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

def upload_to_username(instance, filename):
    return '%s/%s' % (instance.user.username, filename)

def upload_to_root(instance, filename):
    return '%s/%s' % ('./', filename)

class Song(models.Model):
    """
    Song model
    """
    file = models.FileField(_('File'), default='', upload_to=upload_to_username)
    file_size = models.CharField(_('File size in bytes'), max_length=10, blank=True, null=True)
    file_type = models.CharField(_('File type'), max_length=5, blank=True, null=True)
    duration = models.DurationField(_('Song duration'), blank=True, null=True)

    title = models.CharField(_('Title'), max_length=250, blank=True, null=True)
    artist = models.CharField(_('Artist'), max_length=250, blank=True, null=True)
    album = models.CharField(_('Album name'), max_length=500, blank=True, null=True)
    year = models.PositiveSmallIntegerField(
        _('Year'),
        validators=[MaxValueValidator(3000)],
        blank=True,
        null=True
    )
    release_date = models.DateField(_('Complete release date (day-month-year)'), blank=True, null=True)
    album_artist = models.CharField(_('Album artist (band/orchestra/accompaniment)'), max_length=250, blank=True, null=True)
    track_number = models.PositiveSmallIntegerField(
        _('Track number'),
        validators=[MaxValueValidator(3000)],
        blank=True,
        null=True
    )
    track_total = models.PositiveSmallIntegerField(
        _('Total track count'),
        validators=[MaxValueValidator(3000)],
        blank=True, 
        null=True
    )
    bpm = models.FloatField(
        _('Beats per minute'),
        validators=[MinValueValidator(5), MaxValueValidator(300)],
        blank=True,
        null=True
    )
    original_artist = models.CharField(_('Original artist(s)/performer(s)'), max_length=250, blank=True, null=True)
    key = models.CharField(_('Song key'), max_length=50, blank=True, null=True)
    composer = models.CharField(_('Composer'), max_length=250, blank=True, null=True)
    lyricist = models.CharField(_('Lyricist/text writer'), max_length=250, blank=True, null=True)
    comments = models.CharField(_('Comments'), max_length=500, blank=True, null=True)
    remixer = models.CharField(_('Interpreted, remixed or otherwise modified by'), max_length=250, blank=True, null=True)
    label = models.CharField(_('Label/Publisher'), max_length=250, blank=True, null=True)
    genre = models.CharField(_('Genre/content type'), max_length=100, blank=True, null=True)
    lyrics = models.TextField(_('Lyrics'), blank=True, null=True)

    artwork = models.ImageField(_('Attached song cover'), upload_to=upload_to_root, blank=True, null=True)

    slug = models.SlugField(_('Slug'), unique=True, db_index=True)
    ctime = models.DateField(_('Creation time'), auto_now_add=True)
    mtime = models.DateField(_('Modified time'), auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL) # User which this song file belongs to

    # Where to be redirected after you add a new song
    def get_absolute_url(self):
        return reverse('box:detail-update', kwargs={'pk': self.pk})

    def save(self, create= False, update=False, *args, **kwargs):
        if create:
            file_final_path = self.file.path
            file_name = self.file.name
            self.file_type = file_final_path.split('.')[-1].lower()
            file_temp_path = os.path.join(settings.MEDIA_ROOT,'tmp','temp.'+self.file_type)
            default_storage.save(file_temp_path,ContentFile(self.file.file.read()))
            self.file_size = humanize.naturalsize(os.path.getsize(file_temp_path))

            # MP3
            if self.file_type == "mp3":
                mp3_tags_to_song_model(file_name, file_temp_path, self)

            # MP4
            elif self.file_type == "m4a":
                m4a_tags_to_song_model(file_name, file_temp_path, self)

            default_storage.delete(os.path.join(settings.MEDIA_ROOT,'tmp','temp.'+self.file_type))

            # Slug
            slugaux = os.path.splitext(os.path.basename(self.file.name))[0] # Filename without extension
            slugaux = slugaux.replace("_", " ") # Replace '_' by ' '
            slugaux = ' '.join(slugaux.split()) # Leave only one space between words
            self.slug = slugify(slugaux)

            # If there is no 'Title' attribute, use the filename as title
            if not self.title:
                self.title = slugaux

        elif update:
            # MP3
            if self.file_type == "mp3":
                tags_from_song_model_to_mp3(self)

            # MP4
            elif self.file_type == "m4a":
                pass


        super(Song, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.file.name

    #def clean_filename(self):
    #    cleaned_name = (self.file.name).replace("_", " ") # Replace '_' by ' '
    #    cleaned_name = ' '.join(cleaned_name.split()) # Leave only one space between words
    #    cleaned_name = cleaned_name.replace(" ", "_") # Replace ' ' by '_'
    #    return cleaned_name

@receiver(pre_delete, sender=Song)
def song_delete(sender, instance, **kwargs):
    """
    Things to do before delete a song field from the db
    """
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
    instance.artwork.delete(False)
