from rest_framework import viewsets, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from mrp.utils import IsOwnerOrReadOnly, validate_uuid4
from party.models import Party, PartyUser, PartyCategory
from party.serializers import (
    PartySerializer,
    PartyUserSerializer,
    PartyUserCreateSerializer,
    PartyCreateSerializer,
    PartyCategorySerializer,
)


class PartyViewSet(viewsets.ModelViewSet):
    """
    list:
    Get list of parties owned by authenticated user.

    create:
    Create party and join it.
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.action is 'list':
            return Party.objects.filter(user=self.request.user)
        return Party.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return PartyCreateSerializer
        return PartySerializer


class PartyUserViewSet(viewsets.ModelViewSet):
    queryset = PartyUser.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    filter_fields = ('party', 'user',)

    def get_serializer_class(self):
        if self.action is 'create':
            return PartyUserCreateSerializer
        return PartyUserSerializer


class PartyCategoryViewSet(viewsets.ModelViewSet):
    queryset = PartyCategory.objects.all()
    # @fixme Only category party owner should have modification access
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PartyCategorySerializer

    def get_queryset(self):
        """
        Get list by forcing party filter.
        """
        if self.action is 'list':
            party: str = self.request.query_params.get('party')
            if validate_uuid4(party):
                return PartyCategory.objects.filter(party=party, party__user=self.request.user)
            raise exceptions.NotFound()
        return PartyCategory.objects.all()
