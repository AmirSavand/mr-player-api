from uuid import UUID

from django.contrib.auth.models import User
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission

from like.models import Like


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    except TypeError:
        return False
    return True


def get_serializer_like(serializer, obj, kind: Like.Kind) -> int:
    user = serializer.context['request'].user
    if user.is_authenticated:
        like = Like.objects.filter(kind=kind, like=obj.pk, user=user.id)
        if like.exists():
            return like[0].id
        return 0
    return 0


class StandardPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 100


class LargePagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 1000


class IsAuthAndPartyOwnerOrOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        # Allow safe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow authenticated user
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # Allow safe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow if user is owner of party of object
        if request.user == obj.party.user:
            return True

        # Allow if user is owner of object
        return request.user == obj.user


class IsAuthAndOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        # Allow safe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow authenticated user
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # Allow safe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow if user is owner of object
        if type(obj) is not User:
            return request.user == obj.user

        # Allow if user is object
        return request.user == obj


class IsAuthAndOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {
            'subject_template_name': 'templates/email-password-reset-subject.txt',
            'email_template_name': 'templates/email-password-reset.txt'
        }


class Regex:
    YOUTUBE = r'(https?://)?(www\.)?(youtube|youtu)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    SOUNDCLOUD = r'^(https?:\/\/)?(www.)?(m\.)?soundcloud\.com\/[\w\-\.]+(\/)+[\w\-\.]+/?$'
    IMGUR = r'(https?:)?\/\/(\w+\.)?imgur\.com\/(\S*)(\.[a-zA-Z]{3})'
