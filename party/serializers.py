from rest_framework import serializers

from account.serializers import UserSerializer
from party.models import Party, PartyUser


class PartySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    name = serializers.ReadOnlyField()

    class Meta:
        model = Party
        fields = (
            'id',
            'user',
            'name',
            'date',
        )


class PartyCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Party
        fields = (
            'id',
            'user',
            'title',
            'name',
            'date',
        )
        extra_kwargs = {
            'title': {'write_only': True}
        }

    def create(self, validated_data):
        party: Party = Party.objects.create(**validated_data)
        PartyUser.objects.create(party=party, user=validated_data.get('user'))
        return party


class PartyUserSerializer(serializers.ModelSerializer):
    party = PartySerializer()
    user = UserSerializer()

    class Meta:
        model = PartyUser
        fields = '__all__'


class PartyUserCreateSerializer(serializers.ModelSerializer):
    party = serializers.PrimaryKeyRelatedField(queryset=Party.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PartyUser
        fields = (
            'id',
            'party',
            'user',
        )
