from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from dj.models import Dj, DjUser


class DjSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dj
        fields = '__all__'


class DjCreateSerializer(DjSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())


class DjUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjUser
        fields = '__all__'


class DjUserCreateSerializer(DjUserSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
