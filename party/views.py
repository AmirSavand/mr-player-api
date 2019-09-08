from django.db.models import QuerySet, Q
from rest_framework import viewsets, exceptions

from mrp.utils import validate_uuid4, IsAuthAndPartyOwnerOrOwnerOrReadOnly, IsAuthAndOwnerOrReadOnly
from party.models import Party, PartyUser, PartyCategory, PartyStatus
from party.serializers import (
    PartySerializer,
    PartyUserSerializer,
    PartyUserCreateSerializer,
    PartyCreateSerializer,
    PartyCategorySerializer,
)


class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    permission_classes = (IsAuthAndOwnerOrReadOnly,)
    filter_fields = ('status', 'user',)

    def get_queryset(self):
        queryset: QuerySet = self.queryset
        if self.action is 'list':
            if self.request.user.is_authenticated:
                queryset = queryset.filter(Q(user=self.request.user) | Q(status=PartyStatus.PUBLIC))
            else:
                queryset = queryset.filter(status=PartyStatus.PUBLIC)
        elif self.action is 'retrieve':
            if self.request.user.is_authenticated:
                queryset = queryset.filter(Q(user=self.request.user) | ~Q(status=PartyStatus.CLOSE))
            else:
                queryset = queryset.exclude(status=PartyStatus.CLOSE)
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return PartyCreateSerializer
        return PartySerializer


class PartyUserViewSet(viewsets.ModelViewSet):
    queryset = PartyUser.objects.all()
    permission_classes = (IsAuthAndPartyOwnerOrOwnerOrReadOnly,)
    filter_fields = ('party', 'user',)

    def get_serializer_class(self):
        if self.action is 'create':
            return PartyUserCreateSerializer
        return PartyUserSerializer


class PartyCategoryViewSet(viewsets.ModelViewSet):
    queryset = PartyCategory.objects.all()
    permission_classes = (IsAuthAndPartyOwnerOrOwnerOrReadOnly,)
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
