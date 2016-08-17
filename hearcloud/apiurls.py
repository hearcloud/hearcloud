from django.conf.urls import url

from applications.box.api import SongsList

urlpatterns = [
    url(r'^songs/$', SongsList.as_view(), name='songs_list'),
]
