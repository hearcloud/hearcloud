from rest_framework import generics, permissions

from .models import Song
from .permissions import IsOwnerOrSuperuserOrDenyAccess
from .serializers import SongSerializer


class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrSuperuserOrDenyAccess,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
