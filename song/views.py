from rest_framework import permissions, exceptions
from rest_framework.viewsets import ModelViewSet

from mrp.utils import validate_uuid4, LargePagination
from song.models import Song
from song.serializers import SongSerializer, SongCreateSerializer, SongMinimalSerializer, SongUpdateSerializer


class IsSongOrPartyOwnerOrReadOnly(permissions.BasePermission):
    """
    Owner of song or party can modify.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any safe request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of this object or owner of its party
        return obj.user == request.user or obj.party.user == request.user


class SongViewSet(ModelViewSet):
    """
    list:
    Get song list by party only.
    """
    permission_classes = (IsSongOrPartyOwnerOrReadOnly,)
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
        return SongSerializer
