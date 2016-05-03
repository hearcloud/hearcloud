from django.conf.urls import url, include
from rest_framework import routers

from box.api import SongsViewSet

router = routers.DefaultRouter()
router.register(r'songs', SongsViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
