from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from like.models import Like
from like.serializers import LikeSerializer
from playzem.utils import IsAuthAndOwnerOrReadOnly


class LikeViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthAndOwnerOrReadOnly,)
    filterset_fields = ('user', 'kind', 'like',)
