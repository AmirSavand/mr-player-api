from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault

from like.models import Like


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Like
        fields = (
            'id',
            'user',
            'kind',
            'like',
            'date',
        )


class LikeCreateSerializer(LikeSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    def validate(self, data):
        model = Like.get_like_model(data['kind'])
        try:
            model.objects.get(pk=data['like'])
        except (ValueError, ObjectDoesNotExist):
            raise ValidationError('You can not like what does not exist.')
        return super().validate(data)
