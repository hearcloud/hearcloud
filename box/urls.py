from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

# to make namespaces reference only this app (this way we can have 
# the same name in different apps)
app_name = 'box'

urlpatterns = [
    # /box/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /box/<song-id>/
    url(r'^(?P<pk>[0-9]+)/$', login_required(views.SongDetailView.as_view()), name='song-detail'),

    # /box/<song-id>/update
    url(r'^(?P<song_id>[0-9]+)/update/$', login_required(views.SongUpdateView.as_view()), name='song-update'),

    # /box/song/add
    url(r'song/add/$', login_required(views.SongAjaxCreateView.as_view()), name='song-add'),

    # /box/song/<id>/delete
    url(r'song/(?P<song_id>[0-9]+)/delete/$', login_required(views.SongDelete.as_view()), name='song-delete'),
]
