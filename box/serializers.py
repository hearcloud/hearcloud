from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )
    file = serializers.FileField(max_length=None, use_url=True)
    artwork = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Song
        fields = (
          'file', 'file_size', 'file_type', 'duration', 'title', 
          'artist', 'album', 'year', 'release_date', 'album_artist',
          'track_number', 'track_total', 'bpm', 'original_artist',
          'key', 'composer', 'lyricist', 'comments', 'remixer', 'label',
          'genre', 'artwork',
        )
        read_only_fields = ('ctime', 'mtime', 'user')
        #fields = '__all__'
