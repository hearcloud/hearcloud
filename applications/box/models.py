#! -*- codin: utf-8 -*-

from __future__ import unicode_literals

import humanize
import os
import itertools

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from .functions import mp3_tags_to_song_model, tags_from_song_model_to_mp3, m4a_tags_to_song_model, \
    aiff_tags_to_song_model, tags_from_song_model_to_aiff, wav_tags_to_song_model, tags_from_song_model_to_m4a, \
    tags_from_song_model_to_wav


def upload_to_username(instance, filename):
    return '%s/%s' % (instance.user.username, filename)


def upload_to_root(instance, filename):
    return '%s/%s' % ('./', filename)


class Playlist(models.Model):
    """
    Playlist model
    """
    name = models.CharField(_('Playlist name'), max_length=250)
    slug = models.SlugField(_('Slug'), unique=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)  # User which this playlist belongs to

    # Where to be redirected after you add a new playlist
    def get_absolute_url(self):
        return reverse('box:playlist-detail', kwargs={'username': self.user.username, 'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug =  check_slug_exists = slugify(self.name)

        for x in itertools.count(1):
            if not Playlist.objects.filter(slug=self.slug).exists():
                break
            self.slug = '%s-%d' % (check_slug_exists, x)
        return super(Playlist, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.name


class Song(models.Model):
    """
    Song model
    """
    file = models.FileField(_('File'), default='', upload_to=upload_to_username)
    original_filename = models.CharField(_('Original filename'), max_length=250, blank=True, null=True)
    file_size = models.CharField(_('File size in bytes'), max_length=10, blank=True, null=True)
    file_type = models.CharField(_('File type'), max_length=5, blank=True, null=True)
    duration = models.DurationField(_('Song duration'), null=True)

    title = models.CharField(_('Title'), max_length=250, blank=True, null=True)
    artist = models.CharField(_('Artist'), max_length=250, blank=True, null=True)
    album = models.CharField(_('Album name'), max_length=500, blank=True, null=True)
    year = models.PositiveSmallIntegerField(
        _('Year'),
        validators=[MaxValueValidator(3000)],
        blank=True,
        null=True,
    )
    release_date = models.DateField(_('Complete release date (day-month-year)'), blank=True, null=True)
    album_artist = models.CharField(_('Album artist (band/orchestra/accompaniment)'), max_length=250, blank=True,
                                    null=True)
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
    remixer = models.CharField(_('Interpreted, remixed or otherwise modified by'), max_length=250, blank=True,
                               null=True)
    label = models.CharField(_('Label/Publisher'), max_length=250, blank=True, null=True)
    genre = models.CharField(_('Genre/content type'), max_length=100, blank=True, null=True)
    lyrics = models.TextField(_('Lyrics'), blank=True, null=True)

    artwork = models.ImageField(_('Song cover'), upload_to=upload_to_root, null=True, blank=True)

    slug = models.SlugField(_('Slug'), max_length=100, unique=True, db_index=True)
    ctime = models.DateTimeField(_('Creation time'), auto_now_add=True)
    mtime = models.DateTimeField(_('Modified time'), auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)  # User which this song file belongs to
    playlists = models.ManyToManyField(Playlist)

    # Where to be redirected after you add a new song
    def get_absolute_url(self):
        return reverse('box:song-detail', kwargs={'username': self.user.username, 'slug': self.slug})

    def save(self, create=False, update=False, *args, **kwargs):
        if not self.slug:
            slug_final = check_slug_exists = slugify(self.file.name)
            if check_slug_exists != 'add':
                for x in itertools.count(1):
                    if not Song.objects.filter(slug=slug_final).exists():
                        break
                    slug_final = '%s-%d' % (check_slug_exists, x)
            else:
                slug_final = '%s-%d' % (check_slug_exists, 1)
                for x in itertools.count(1):
                    if not Song.objects.filter(slug=slug_final).exists():
                        break
                    slug_final = '%s-%d' % (check_slug_exists, x)

            self.slug = slug_final

        if create:
            file_final_path = self.file.path
            file_name = self.file.name
            self.file_type = file_final_path.split('.')[-1].lower()
            file_temp_path = os.path.join(settings.MEDIA_ROOT, 'tmp', 'temp.' + self.file_type)
            default_storage.save(file_temp_path, ContentFile(self.file.file.read()))
            self.file_size = humanize.naturalsize(os.path.getsize(file_temp_path))

            # MP3
            if self.file_type == "mp3":
                mp3_tags_to_song_model(file_name, file_temp_path, self)

            # MP4
            elif self.file_type == "m4a":
                m4a_tags_to_song_model(file_name, file_temp_path, self)

            # AIF or AIFF, it's the same
            elif self.file_type == "aif" or self.file_type == "aiff":
                if self.file_type == "aif":
                    self.file_type = "aiff"
                aiff_tags_to_song_model(file_name, file_temp_path, self)

            # WAV
            elif self.file_type == "wav":
                wav_tags_to_song_model(file_name, file_temp_path, self)

            default_storage.delete(os.path.join(settings.MEDIA_ROOT, 'tmp', 'temp.' + self.file_type))

            # Slug
            slugaux = os.path.splitext(os.path.basename(self.original_filename))[0]  # Filename without extension
            slugaux = slugaux.replace("_", " ")  # Replace '_' by ' '
            slugaux = ' '.join(slugaux.split())  # Leave only one space between words

            check_slug_exists = slugify(slugaux)
            if not Song.objects.filter(slug=check_slug_exists).exists() and check_slug_exists != 'add':
                self.slug = slugify(slugaux)

            else:
                slug_final = check_slug_exists

                if check_slug_exists != 'add':
                    for x in itertools.count(1):
                        if not Song.objects.filter(slug=slug_final).exists():
                            break
                        slug_final = '%s-%d' % (check_slug_exists, x)
                else:
                    slug_final = '%s-%d' % (check_slug_exists, 1)
                    for x in itertools.count(1):
                        if not Song.objects.filter(slug=slug_final).exists():
                            break
                        slug_final = '%s-%d' % (check_slug_exists, x)

                self.slug = slug_final

            if not self.title:
                self.title = slugaux

        elif update:
            # MP3
            if self.file_type == "mp3":
                tags_from_song_model_to_mp3(song=self, file_path=self.file.path)

            # MP4
            elif self.file_type == "m4a":
                tags_from_song_model_to_m4a(song=self, file_path=self.file.path)

            # AIFF
            elif self.file_type == "aiff":
                tags_from_song_model_to_aiff(song=self, file_path=self.file.path)

            # WAV
            elif self.file_type == "wav":
                tags_from_song_model_to_wav(song=self, file_path=self.file.path)

        return super(Song, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

        # def clean_filename(self):
        #    cleaned_name = (self.file.name).replace("_", " ") # Replace '_' by ' '
        #    cleaned_name = ' '.join(cleaned_name.split()) # Leave only one space between words
        #    cleaned_name = cleaned_name.replace(" ", "_") # Replace ' ' by '_'
        #    return cleaned_name

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        self.artwork.delete(False)
        super(Song, self).delete(*args, **kwargs)

    def artwork_tag(self):
        return u'<img src="%s" width="100" height="100"/>' % self.artwork.url

    artwork_tag.short_description = 'Artwork'
    artwork_tag.allow_tags = True

    def get_filename(self):
        return os.path.splitext(self.original_filename)[0]
