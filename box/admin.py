from django.contrib import admin
from .models import Song

class SongAdmin(admin.ModelAdmin):
    """
    Admin class to view, update, create or delete new Song models
    """
    list_display = ('audio_file', 'song_title', 'artist', 'duration', 'uuid')
    readonly_fields = ("uuid", "duration", "mime_type")

admin.site.register(Song, SongAdmin)
