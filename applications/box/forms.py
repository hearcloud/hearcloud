from django import forms
from django.core.exceptions import ValidationError 

from .models import Song

# Allowed file types
file_TYPES = ['mp3', 'wav', 'm4a']


class UpdateSongForm(forms.ModelForm):
    """
    Form class to update already created songs on the db
    """
    title = forms.CharField(
        max_length=Song._meta.get_field('title').max_length,
        required=False
    )
    artist = forms.CharField(
        max_length=Song._meta.get_field('artist').max_length,
        required=False
    )
    year = forms.IntegerField(required=False)
    release_date = forms.DateField(required=False)
    album_artist = forms.CharField(
        max_length=Song._meta.get_field('album_artist').max_length,
        required=False
    )
    track_number = forms.IntegerField(required=False)
    track_total = forms.IntegerField(required=False)
    bpm = forms.FloatField(required=False)
    original_artist = forms.CharField(
        max_length=Song._meta.get_field('original_artist').max_length,
        required=False
    )
    key = forms.CharField(
        max_length=Song._meta.get_field('key').max_length,
        required=False
    )
    composer = forms.CharField(
        max_length=Song._meta.get_field('composer').max_length,
        required=False
    )
    lyricist = forms.CharField(
        max_length=Song._meta.get_field('lyricist').max_length,
        required=False
    )
    comments = forms.CharField(
        max_length=Song._meta.get_field('comments').max_length,
        required=False
    )
    remixer = forms.CharField(
        max_length=Song._meta.get_field('remixer').max_length,
        required=False
    )
    label = forms.CharField(
        max_length=Song._meta.get_field('label').max_length,
        required=False
    )
    genre = forms.CharField(
        max_length=Song._meta.get_field('genre').max_length,
        required=False
    )
    lyrics = forms.CharField(
        required=False,
        widget=forms.Textarea
    )
    artwork = forms.ImageField(required=False)

    class Meta:
        model = Song
        fields = [
            'artwork', 'title', 'artist', 'year', 'album',
            'release_date', 'album_artist', 'track_number', 'bpm', 
            'original_artist', 'key', 'composer', 'lyricist', 'comments',
            'remixer', 'label', 'genre'
        ]

    def save(self, commit=True):
        instance = super(UpdateSongForm, self).save(commit=False)

        if commit:
            # save
            instance.save()

        return instance
