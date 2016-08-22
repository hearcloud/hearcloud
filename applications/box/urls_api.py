from django.conf.urls import include, url

from .views_api import SongList

urlpatterns = [
    url(r'^songs/$', SongList.as_view(), name='song_list'),
]
