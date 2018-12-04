from rest_framework import viewsets

from mrp.utils import StandardPagination, IsOwnerOrReadOnly
from song.models import Song, SongParty
from song.serializers import SongSerializer, SongPartySerializer, SongCreateSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    pagination_class = StandardPagination
    serializer_class = SongSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    http_method_names = ('get', 'post', 'delete')

    def get_serializer_class(self):
        if self.action == 'create':
            return SongCreateSerializer
        return self.serializer_class


class SongPartyViewSet(viewsets.ModelViewSet):
    queryset = SongParty.objects.all()
    pagination_class = StandardPagination
    serializer_class = SongPartySerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'key'
