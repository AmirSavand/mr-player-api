from django.contrib.auth.models import User
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from account.serializers import UserSerializer


class UserViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Get user detail and sign up.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


def jwt_response_payload_handler(token, user=None, request=None) -> dict:
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
    }
