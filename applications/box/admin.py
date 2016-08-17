from django.contrib import admin
from .models import Song

from django.utils.translation import ugettext_lazy as _


class SongAdmin(admin.ModelAdmin):
    """
    Admin class to view, update, create or delete new Song models
    """
    list_display = ('title', 'artist', 'duration', 'file')
    readonly_fields = ('duration', 'file_size', 'file_type', 'slug', 'artwork_tag', 'ctime', 'mtime')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj = Song.objects.create(user=request.user, file=form.cleaned_data['file'])
        obj.save(create=True)

    def get_fieldsets(self, request, obj=None):
        if obj: # this is a change form
            fieldsets = [
                (_('FILE'), {
                    'fields': [
                        ('file', 'file_size', 'file_type'),
                        ('duration'),
                        ('ctime'),
                        ('mtime'),
                    ]
                }),
                (_('METADATA'), {
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
