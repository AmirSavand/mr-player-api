from django.db.models import QuerySet, Q
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from party.models import Party, PartyUser, PartyCategory
from party.serializers import (
    PartySerializer,
    PartyUserSerializer,
    PartyUserCreateSerializer,
    PartyCreateSerializer,
    PartyCategorySerializer,
)
from playzem.utils import IsAuthAndPartyOwnerOrOwnerOrReadOnly, IsAuthAndOwnerOrReadOnly


class PartyViewSet(ModelViewSet):
    queryset = Party.objects.all()
    permission_classes = (IsAuthAndOwnerOrReadOnly,)
    filter_fields = ('status', 'user',)
    order_fields = ('date',)
    search_fields = (
        'title',
        'description',
        'party_category__name',
        'user__username',
        'user__account__display_name',
    )

    def get_queryset(self):
        queryset: QuerySet = self.queryset
        if self.action is 'list':
            if self.request.user.is_authenticated:
                queryset = queryset.filter(Q(user=self.request.user) | Q(status=Party.Status.PUBLIC))
            else:
                queryset = queryset.filter(status=Party.Status.PUBLIC)
        elif self.action is 'retrieve':
            if self.request.user.is_authenticated:
                queryset = queryset.filter(Q(user=self.request.user) | ~Q(status=Party.Status.CLOSE))
            else:
                queryset = queryset.exclude(status=Party.Status.CLOSE)
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return PartyCreateSerializer
        return PartySerializer


class PartyUserViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = PartyUser.objects.all()
    permission_classes = (IsAuthAndPartyOwnerOrOwnerOrReadOnly,)
    filter_fields = ('party', 'user',)

    def get_serializer_class(self):
        if self.action is 'create':
            return PartyUserCreateSerializer
        return PartyUserSerializer


class PartyCategoryViewSet(ModelViewSet):
    queryset = PartyCategory.objects.all()
    permission_classes = (IsAuthAndPartyOwnerOrOwnerOrReadOnly,)
    serializer_class = PartyCategorySerializer
    filter_fields = ('party',)
