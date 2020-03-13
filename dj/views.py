from rest_framework.viewsets import ModelViewSet

from dj.models import Dj, DjUser
from dj.serializers import DjSerializer, DjCreateSerializer, DjUserCreateSerializer, DjUserSerializer
from playsem.utils import IsAuthAndOwnerOrReadOnly


class DjViewSet(ModelViewSet):
    queryset = Dj.objects.all()
    permission_classes = (IsAuthAndOwnerOrReadOnly,)
    filter_fields = ('party',)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return DjCreateSerializer
        return DjSerializer


class DjUserViewSet(ModelViewSet):
    queryset = DjUser.objects.all()
    permission_classes = (IsAuthAndOwnerOrReadOnly,)
    filter_fields = ('dj',)

    def get_serializer_class(self):
        if self.action == 'create':
            return DjUserCreateSerializer
        return DjUserSerializer
