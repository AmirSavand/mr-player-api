from rest_framework import serializers

from account.serializers import UserSerializer
from song.models import Song, SongParty


class SongPartySerializer(serializers.ModelSerializer):
    user = UserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = SongParty
        exclude = (
            'key',
        )


class SongSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    party = SongPartySerializer()

    class Meta:
        model = Song
        fields = '__all__'


class SongCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    party = serializers.SlugRelatedField(slug_field='key', queryset=SongParty.objects.all())

    class Meta:
        model = Song
        fields = (
            'user',
            'party',
            'source',
        )
