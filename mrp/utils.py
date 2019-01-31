from uuid import UUID

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    except TypeError:
        return False
    return True


class StandardPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 100


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any safe request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed for authenticated users
        if not request.user.is_authenticated:
            return False

        # Write permissions are only allowed to the owner of this object
        if type(obj) is not User:
            return obj.user == request.user

        # Write permissions are only allowed to the authenticated user
        return obj == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of object.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user


class Regex:
    """
    Regex patterns for songs source.
    """
    YOUTUBE = r'(https?://)?(www\.)?(youtube|youtu)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    SOUNDCLOUD = r'^(https?:\/\/)?(www.)?(m\.)?soundcloud\.com\/[\w\-\.]+(\/)+[\w\-\.]+/?$'
