from django.contrib import admin
from .models import Song

class SongAdmin(admin.ModelAdmin):
    """
    Admin class to view, update, create or delete new Song models
    """
    list_display = ('file', 'title', 'artist', 'duration')
    readonly_fields = ('duration', 'file_size', 'file_type')

admin.site.register(Song, SongAdmin)
