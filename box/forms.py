from django import forms
from django.core.exceptions import ValidationError 

from .models import Song

# Allowed file types
AUDIO_FILE_TYPES = ['mp3', 'wav', 'm4a']

class SongForm(forms.ModelForm):
    """
    Form class to create songs on the db
    """
    def clean_audio_file(self):
        file = self.cleaned_data.get("audio_file", False)
        filetype = file.name.split('.')[-1].lower()
        if filetype not in AUDIO_FILE_TYPES:
            raise ValidationError("Audio file must be WAV or MP3")
        return file

    # Info about the class
    class Meta:
        model = Song
        fields = ['audio_file']



class UpdateSongForm(forms.ModelForm):
    """
    Form class to update already created songs on the db
    """
    song_title = forms.CharField(
        max_length=Song._meta.get_field('song_title').max_length
    )
    artist = forms.CharField(
        max_length=Song._meta.get_field('artist').max_length
    )

    class Meta:
        model = Song
        fields = ['artwork', 'song_title', 'artist', 'year', 'album', 
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
