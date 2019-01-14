import re

import requests
from django.http import request
from requests import Response
from rest_framework import serializers
from rest_framework.utils import json

from account.serializers import UserSerializer
from mrp.utils import Regex
from party.models import Party
from party.serializers import PartySerializer
from song.models import Song, SongPlayer


class SongSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    party = PartySerializer(read_only=True)

    class Meta:
        model = Song
        fields = '__all__'


class SongCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    party = serializers.PrimaryKeyRelatedField(queryset=Party.objects.all())

    class Meta:
        model = Song
        fields = '__all__'
        extra_kwargs = {
            'player': {'read_only': True}
        }

    def create(self, validated_data):
        data: dict = validated_data

        # Set user to authenticated user
        data['user'] = self.context['request'].user

        # Check source for youtube player
        if re.match(Regex.YOUTUBE, data['source']):
            data['player'] = SongPlayer.YOUTUBE

        # Check source for soundcloud player
        elif re.match(Regex.SOUNDCLOUD, data['source']):
            data['player'] = SongPlayer.SOUNDCLOUD

        # Source didn't match any player
        else:
            raise serializers.ValidationError({'error': 'Invalid YouTube or SoundCloud URL.'})

        # Get song name if not set
        if not data['name']:
            if data['player'] == SongPlayer.YOUTUBE:
                response: Response = requests.get('https://youtube.com/oembed', {
                    'url': data['source'],
                    'format': 'json',
                })
                data['name'] = response.json()['title']

        return super().create(data)
