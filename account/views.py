from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from account.models import Account
from account.serializers import UserSerializer, AccountSerializer
from playsem.utils import IsAuthAndOwnerOrReadOnly


class UserViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        obj = get_object_or_404(queryset.filter(
            Q(username=self.kwargs['username']) | Q(pk=self.request.query_params.get('pk'))
        ))
        self.check_object_permissions(self.request, obj)
        return obj


class AccountViewSet(UpdateModelMixin, GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthAndOwnerOrReadOnly,)
    lookup_field = 'user__username'


def jwt_response_payload_handler(token, user=None, request=None) -> dict:
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
    }
