from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    """
    Form class to create songs on the db
    """
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
