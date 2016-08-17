from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

# to make namespaces reference only this app (this way we can have
# the same name in different apps)
app_name = 'box'

urlpatterns = [
    # /box/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /box/song/add
    url(r'song/add/$', login_required(views.SongCreateView.as_view()), name='song-add'),
    #url(r'song/add/view/$', login_required(views.SongListView.as_view()), name='song-add-view'),

    # /box/<username>/<song-slug>/
    url(r'^(?P<username>[\w.@+-]+)/(?!playlists)(?P<slug>[\w.-]{0,256})/$', login_required(views.SongDetailView.as_view()),
        name='song-detail'),

    # /box/<username>/<song-slug>/download
    url(r'^(?P<username>[\w.@+-]+)/(?!playlists)(?P<slug>[\w.-]{0,256})/download/$', login_required(views.song_download),
        name='song-download'),

    # /box/<username>/<song-slug>/update
    url(r'^(?P<username>[\w.@+-]+)/(?!playlists)(?P<slug>[\w.-]{0,256})/update/$', login_required(views.SongUpdateView.as_view()),
        name='song-update'),

    # /box/song/<username>/<song-slug>/delete-
    url(r'song/(?P<username>[\w.@+-]+)/(?P<slug>[\w.-]{0,256})/delete/$', login_required(views.SongDelete.as_view()),
        name='song-delete'),

    # /box/search
    url(r'^search/$', views.song_search, name='song-search'),

    # /box/<username>/playlists
    url(r'^(?P<username>[\w.@+-]+)/playlists/$', login_required(views.PlaylistListView.as_view()),
        name='playlist-list'),

    # /box/<username>/playlists/add
    url(r'^(?P<username>[\w.@+-]+)/playlists/add/$', login_required(views.PlaylistCreateView.as_view()),
        name='playlist-add'),
]
