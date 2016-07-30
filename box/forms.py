from django import forms
from django.core.exceptions import ValidationError 

from .models import Song

from multiupload.fields import MultiMediaField

# Allowed file types
file_TYPES = ['mp3', 'wav', 'm4a']

class UploadSongForm(forms.ModelForm):
    """
    Form class to create songs on the db
    """
    files = MultiMediaField(
        min_num=1, 
        max_num=3, 
        max_file_size=1024*1024*30, 
        media_type='audio'  # 'audio', 'video' or 'image'
    )

    def clean_file(self):
        for file in self.cleaned_data.get("file", False):
            filetype = file.name.split('.')[-1].lower()
            if filetype not in file_TYPES:
                raise ValidationError("Audio file" + file.name + " must be M4A, WAV or MP3")
            return file

    # Info about the class
    class Meta:
        model = Song
        fields = ['files']



class UpdateSongForm(forms.ModelForm):
    """
    Form class to update already created songs on the db
    """
    title = forms.CharField(
        max_length=Song._meta.get_field('title').max_length
    )
    artist = forms.CharField(
        max_length=Song._meta.get_field('artist').max_length
    )

    class Meta:
        model = Song
        fields = ['artwork', 'title', 'artist', 'year', 'album', 
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
