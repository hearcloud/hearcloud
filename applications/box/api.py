from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Song
from .permissions import IsOwnerOrDenyAccess
from .serializers import SongSerializer


class SongMixin(object):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrDenyAccess,)

    def pre_save(self, obj):
        obj.user = self.request.user


class SongsList(SongMixin, APIView):

    @staticmethod
    def get(request):
        if not request.user.is_authenticated():
            # songs = Song.objects.filter(user=self.request.user).order_by('title')
            songs = Song.objects.all()
            serializer = SongSerializer(songs, many=True)
            return Response(serializer.data)
        # return redirect('home:index')

    def post(self):
        pass
