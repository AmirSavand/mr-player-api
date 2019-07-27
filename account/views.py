from django.contrib.auth.models import User
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from account.models import Account
from account.serializers import UserSerializer, AccountSerializer
from mrp.utils import IsAuthAndOwnerOrReadOnly


class UserViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Get user detail and sign up.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class AccountViewSet(UpdateModelMixin, GenericViewSet):
    """
    Update user account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthAndOwnerOrReadOnly,)
    lookup_field = 'user__username'


def jwt_response_payload_handler(token, user=None, request=None) -> dict:
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
    }
