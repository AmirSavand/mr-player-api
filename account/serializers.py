from django.contrib.auth.models import User
from rest_framework import serializers

from account.models import Account
from like.models import Like
from playzem.utils import Regex, get_serializer_like


class AccountSerializer(serializers.ModelSerializer):
    image = serializers.RegexField(Regex.IMGUR, allow_blank=True, allow_null=True)
    name = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = (
            'display_name',
            'image',
            'bio',
            'color',
            'name',
        )
        extra_kwargs = {
            'display_name': {'write_only': True},
        }


class AccountMinimalSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = (
            'color',
            'name',
        )


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    account = AccountSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'date_joined',
            'last_login',
            'likes',
            'like',
            'account',
            'password',
        )
        extra_kwargs = {
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
            'password': {'write_only': True},
        }

    def get_likes(self, obj):
        return Like.objects.filter(kind=Like.Kind.USER, like=obj.pk).count()

    def get_like(self, obj) -> int:
        return get_serializer_like(self, obj, Like.Kind.USER)

    def create(self, validated_data: dict):
        return User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )


class UserMinimalSerializer(serializers.ModelSerializer):
    account = AccountMinimalSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'account',
        )
