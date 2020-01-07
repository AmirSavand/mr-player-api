from typing import Union, Type

from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from party.models import Party, PartyCategory
from party.pusher import get_channel_name
from playzem.pusher import model_trigger
from song.models import Song


class Like(models.Model):
    class Kind(models.IntegerChoices):
        USER = 1
        PARTY = 2
        CATEGORY = 3
        SONG = 4

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.IntegerField(choices=Kind.choices, db_index=True)
    like = models.CharField(max_length=100, db_index=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def like_object(self) -> Union[User, Party, PartyCategory, Song]:
        if self.kind == Like.Kind.USER:
            return User.objects.get(username=self.like)
        if self.kind == Like.Kind.PARTY:
            return Party.objects.get(pk=self.like)
        if self.kind == Like.Kind.CATEGORY:
            return PartyCategory.objects.get(pk=self.like)
        if self.kind == Like.Kind.SONG:
            return Song.objects.get(pk=self.like)

    def __str__(self):
        return '{user} likes a {kind}: {like_object}'.format(
            user=self.user,
            kind=str.lower(self.get_kind_display()),
            like_object=self.like_object,
        )

    class Meta:
        ordering = ('id',)
        unique_together = (('user', 'kind', 'like'),)


@receiver([post_save, post_delete], sender=Like)
def trigger_pusher_like(sender, instance, created=None, **kwargs):
    """
    Trigger pusher for liking a party, category or song
    """
    # No pusher trigger for a user being liked (not party related)
    if instance.kind != Like.Kind.USER:
        model_trigger(instance, created, get_channel_name(
            instance.like_object.pk if instance.kind == Like.Kind.PARTY else instance.like_object.party.pk
        ))


@receiver(post_delete, sender=User)
def delete_user_like(sender, instance, **kwargs):
    # Delete all like objects to this instance
    Like.objects.filter(kind=Like.Kind.USER, like=instance.pk).delete()


@receiver(post_delete, sender=Party)
def delete_party_like(sender, instance, **kwargs):
    # Delete all like objects to this instance
    Like.objects.filter(kind=Like.Kind.PARTY, like=instance.pk).delete()


@receiver(post_delete, sender=PartyCategory)
def delete_party_category_like(sender, instance, **kwargs):
    # Delete all like objects to this instance
    Like.objects.filter(kind=Like.Kind.CATEGORY, like=instance.pk).delete()


@receiver(post_delete, sender=Song)
def delete_song_like(sender, instance, **kwargs):
    # Delete all like objects to this instance
    Like.objects.filter(kind=Like.Kind.SONG, like=instance.pk).delete()
