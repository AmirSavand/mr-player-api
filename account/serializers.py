from django.contrib.auth.models import User
from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = (
            'id',
            'user',
        )


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    account = AccountSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'date_joined',
            'last_login',
            'account',
            'password',
        )
        extra_kwargs = {
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data: dict):
        return User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )
