from django.conf.urls import url, include
from rest_framework import routers

from box.api import SongsList

#router = routers.DefaultRouter()
#router.register(r'songs', SongsViewSet)

urlpatterns = [
    url(r'^songs/$', SongsList.as_view(), name='songs_list'),
]
