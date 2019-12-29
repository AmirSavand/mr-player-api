from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from account.serializers import UserSerializer
from like.models import Like
from playzem.utils import Regex
from party.models import Party, PartyUser, PartyCategory


class PartyCategorySerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PartyCategory
        fields = (
            'id',
            'party',
            'name',
            'image',
            'likes',
        )
        validators = [
            UniqueTogetherValidator(
                message='Category with this name already exists.',
                fields=('party', 'name'),
                queryset=PartyCategory.objects.all(),
            )
        ]

    def get_likes(self, obj):
        return Like.objects.filter(kind=Like.Kind.CATEGORY, like=obj.pk).count()


class PartyCategoryMinimalSerializer(PartyCategorySerializer):
    class Meta:
        model = PartyCategory
        fields = (
            'id',
            'name',
            'image',
            'likes',
        )


class PartySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    name = serializers.ReadOnlyField()
    image = serializers.RegexField(Regex.IMGUR, allow_blank=True, allow_null=True)
    cover = serializers.RegexField(Regex.IMGUR, allow_blank=True, allow_null=True)
    categories = PartyCategoryMinimalSerializer(many=True, source='party_category')
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Party
        fields = (
            'id',
            'user',
            'name',
            'description',
            'status',
            'image',
            'cover',
            'date',
            'likes',
            'categories',
        )

    def get_likes(self, obj):
        return Like.objects.filter(kind=Like.Kind.PARTY, like=obj.pk).count()


class PartyCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.RegexField(Regex.IMGUR, allow_blank=True, allow_null=True)
    cover = serializers.RegexField(Regex.IMGUR, allow_blank=True, allow_null=True)

    class Meta:
        model = Party
        fields = (
            'id',
            'user',
            'title',
            'name',
            'description',
            'status',
            'image',
            'cover',
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
