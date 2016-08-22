from django.contrib import admin
from .models import Song, Playlist

from django.utils.translation import ugettext_lazy as _

class SongInline(admin.TabularInline):
    model = Song.playlists.through
    extra = 1
    verbose_name = 'Song'
    verbose_name_plural = 'Songs in this playlist'

class PlaylistAdmin(admin.ModelAdmin):
    """
    Admin class to view, update, create or delete new Playlist models
    """
    list_display = ('name', 'user')
    readonly_fields = ('user',)
    inlines = [
        SongInline,
    ]

class SongAdmin(admin.ModelAdmin):
    """
    Admin class to view, update, create or delete new Song models
    """
    list_display = ('title', 'artist', 'duration', 'file')
    readonly_fields = ('duration', 'file_size', 'file_type', 'slug', 'artwork_tag', 'ctime', 'mtime', 'user')
    suit_form_tabs = (('file', 'File'), ('song', 'Song'),
                 ('metadata', 'Metadata'))
    filter_horizontal = ('playlists',) 

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj = Song.objects.create(user=request.user, file=form.cleaned_data['file'])
        obj.save(create=True)

    def get_fieldsets(self, request, obj=None):
        if obj: # this is a change form
            fieldsets = [
                (_('FILE'), {
                    'classes': ('suit-tab', 'suit-tab-file',),
                    'fields': [
                        ('file', 'file_size', 'file_type'),
                        ('ctime'),
                        ('mtime'),
                    ]
                }),
                (_('SONG'), {
                    'classes': ('suit-tab', 'suit-tab-song',),
                    'fields': [
                        ('duration'),
                        ('user'),
                        ('playlists'),
                    ]
                }),                
                (_('METADATA'), {
                    'classes': ('suit-tab', 'suit-tab-metadata',),
                    'fields': [
                        ('artwork', 'artwork_tag'),
                        ('title'),
                        ('artist'),
                        ('album'),
                        ('release_date', 'year'),
                        ('album_artist'),
                        ('track_number', 'track_total'),
                        ('original_artist'),
                        ('bpm', 'key'),
                        ('composer', 'lyricist'),
                        ('lyrics', 'comments'),
                        ('remixer', 'label'),
                        ('genre'),
                    ]
                }),
            ]
        else: # this is an add form
            fieldsets = [
                  (None, {
                    'fields': [
                        ('file')
                    ]
                  })
            ]
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj: # Editing
            return self.readonly_fields
        return ()

admin.site.register(Song, SongAdmin)
admin.site.register(Playlist, PlaylistAdmin)
