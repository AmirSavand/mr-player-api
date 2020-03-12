from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from dj.models import Dj, DjUser


class DjSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dj
        fields = '__all__'

    def update(self, instance, validated_data):
        if not validated_data.get('time'):
            validated_data['time'] = '00:00:00'
        return super().update(instance, validated_data)


class DjCreateSerializer(DjSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())


class DjUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjUser
        fields = '__all__'


class DjUserCreateSerializer(DjUserSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
