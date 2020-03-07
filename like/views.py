from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from like.models import Like
from like.serializers import LikeSerializer, LikeCreateSerializer
from playsem.utils import IsAuthAndOwnerOrReadOnly


class LikeViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = Like.objects.all()
    permission_classes = (IsAuthAndOwnerOrReadOnly,)
    filter_fields = ('user', 'kind', 'like',)

    def get_serializer_class(self):
        if self.action in ['create']:
            return LikeCreateSerializer
        return LikeSerializer
