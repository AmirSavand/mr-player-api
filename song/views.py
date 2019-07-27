from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet

from mrp.utils import validate_uuid4, LargePagination, IsAuthAndPartyOwnerOrOwnerOrReadOnly
from song.models import Song
from song.serializers import SongSerializer, SongCreateSerializer, SongMinimalSerializer, SongUpdateSerializer


class SongViewSet(ModelViewSet):
    """
    list:
    Get song list by party only.
    """
    permission_classes = (IsAuthAndPartyOwnerOrOwnerOrReadOnly,)
    pagination_class = LargePagination

    def get_queryset(self):
        """
        Get list by forcing party filter.
        """
        if self.action is 'list':
            party: str = self.request.query_params.get('party')
            if validate_uuid4(party):
                return Song.objects.filter(party=party)
            raise exceptions.NotFound()
        return Song.objects.all()

    def get_serializer_class(self):
        if self.action is 'create':
            return SongCreateSerializer
        if self.action in 'list':
            return SongMinimalSerializer
        if self.action in 'update':
            return SongUpdateSerializer
        return SongSerializer
