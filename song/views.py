from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from playzem.utils import LargePagination, IsAuthAndPartyOwnerOrOwnerOrReadOnly
from song.models import Song, SongCategory
from song.serializers import (
    SongSerializer,
    SongWriteSerializer,
    SongMinimalSerializer,
    SongCategorySerializer,
    SongCategoryWriteSerializer,
)


class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    permission_classes = (IsAuthAndPartyOwnerOrOwnerOrReadOnly,)
    pagination_class = LargePagination
    filter_fields = ('party', 'song_category',)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SongWriteSerializer
        if self.action in 'list':
            return SongMinimalSerializer
        return SongSerializer


class SongCategoryViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = SongCategory.objects.all()
    permission_classes = (IsAuthAndPartyOwnerOrOwnerOrReadOnly,)
    serializer_class = SongCategorySerializer
    pagination_class = LargePagination
    filter_fields = ('song__party', 'song', 'category')

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SongCategoryWriteSerializer
        return SongCategorySerializer
