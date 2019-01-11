from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from mrp.utils import IsOwnerOrReadOnly
from party.models import Party, PartyUser
from party.serializers import PartySerializer, PartyUserSerializer, PartyUserCreateSerializer, PartyCreateSerializer


class PartyViewSet(viewsets.ModelViewSet):
    """
    list:
    Get list of parties owned by authenticated user.

    create:
    Create party and join it.
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

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
    serializer_class = PartyUserSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_fields = ('party', 'user',)

    def get_serializer_class(self):
        if self.action is 'create':
            return PartyUserCreateSerializer
        return PartyUserSerializer
