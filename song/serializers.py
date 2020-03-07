import re

import requests
from requests import Response
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from account.serializers import UserSerializer, UserMinimalSerializer
from like.models import Like
from party.models import Party
from party.serializers import PartySerializer, PartyCategoryMinimalSerializer
from playsem.utils import Regex, get_serializer_like
from song.models import Song, SongCategory


class SongCategorySerializer(serializers.ModelSerializer):
    category = PartyCategoryMinimalSerializer()

    class Meta:
        model = SongCategory
        fields = (
            'id',
            'song',
            'category',
            'date',
        )


class SongCategoryMinimalSerializer(serializers.ModelSerializer):
    category = PartyCategoryMinimalSerializer()

    class Meta:
        model = SongCategory
        fields = (
            'id',
            'category',
        )


class SongCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongCategory
        fields = (
            'id',
            'song',
            'category',
            'date',
        )
        validators = [
            UniqueTogetherValidator(
                message='Song already part of this category.',
                fields=('song', 'category'),
                queryset=SongCategory.objects.all(),
            )
        ]


class SongSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    party = PartySerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Song
        fields = (
            'id',
            'user',
            'party',
            'player',
            'source',
            'name',
            'date',
            'likes',
            'like',
        )

    def get_likes(self, obj):
        return Like.objects.filter(kind=Like.Kind.SONG, like=obj.pk).count()

    def get_like(self, obj) -> int:
        return get_serializer_like(self, obj, Like.Kind.SONG)


class SongMinimalSerializer(SongSerializer):
    user = UserMinimalSerializer()
    categories = SongCategoryMinimalSerializer(many=True, source='song_category')

    class Meta:
        model = Song
        fields = (
            'id',
            'user',
            'player',
            'source',
            'name',
            'categories',
            'likes',
            'like',
        )


class SongWriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    party = serializers.PrimaryKeyRelatedField(queryset=Party.objects.all())

    class Meta:
        model = Song
        fields = '__all__'
        extra_kwargs = {
            'player': {'read_only': True}
        }

    def create(self, validated_data):
        data = validated_data

        # Set user to authenticated user
        data['user'] = self.context['request'].user

        # Check source for youtube player
        if re.match(Regex.YOUTUBE, data['source']):
            data['player'] = Song.Player.YOUTUBE

        # Check source for soundcloud player
        elif re.match(Regex.SOUNDCLOUD, data['source']):
            data['player'] = Song.Player.SOUNDCLOUD

        # Source didn't match any player
        else:
            raise serializers.ValidationError({'error': 'Invalid YouTube or SoundCloud URL.'})

        # Get song name if not set
        if not data.get('name'):
            if data['player'] == Song.Player.YOUTUBE:
                response: Response = requests.get('https://youtube.com/oembed', {
                    'url': data['source'],
                    'format': 'json',
                })
                data['name'] = response.json()['title']

        return super().create(validated_data)
