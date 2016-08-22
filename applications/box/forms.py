from django import forms
from django.core.exceptions import ValidationError 

from .models import Song, Playlist


class CreatePlaylistForm(forms.ModelForm):
    """
    Form class to create playlists
    """

    class Meta:
        model = Playlist
        fields = [
            'name',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class UpdateSongForm(forms.ModelForm):
    """
    Form class to update already created songs on the db
    """

    class Meta:
        model = Song
        fields = [
            'artwork', 'title', 'artist', 'year', 'album',
            'release_date', 'album_artist', 'track_number', 'track_total', 'bpm',
            'original_artist', 'key', 'composer', 'lyricist', 'comments',
            'remixer', 'label', 'genre', 'file', 'lyrics',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'artist': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'album': forms.TextInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control'}),
            'album_artist': forms.TextInput(attrs={'class': 'form-control'}),
            'track_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'track_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'bpm': forms.NumberInput(attrs={'class': 'form-control'}),
            'original_artist': forms.TextInput(attrs={'class': 'form-control'}),
            'key': forms.TextInput(attrs={'class': 'form-control'}),
            'composer': forms.TextInput(attrs={'class': 'form-control'}),
            'lyricist': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.TextInput(attrs={'class': 'form-control'}),
            'remixer': forms.TextInput(attrs={'class': 'form-control'}),
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.TextInput(attrs={'class': 'form-control'}),
            'lyrics': forms.Textarea(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        instance = super(UpdateSongForm, self).save(commit=False)

        if commit:
            # save
            instance.save()

        return instance
