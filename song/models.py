from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from party.models import Party, PartyCategory
from playsem.pusher import model_trigger


class Song(models.Model):
    class Player(models.IntegerChoices):
        YOUTUBE = 1
        SOUNDCLOUD = 2

    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, db_index=True, on_delete=models.CASCADE)
    player = models.IntegerField(choices=Player.choices, default=Player.YOUTUBE)
    source = models.URLField()
    name = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class SongCategory(models.Model):
    song = models.ForeignKey(
        Song, related_name='song_category', db_index=True, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        PartyCategory, related_name='song_category', db_index=True, on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)

    @property
    def party(self):
        return self.category.party

    def __str__(self):
        return '{song} part of {category}'.format(song=self.song, category=self.category)

    class Meta:
        verbose_name_plural = 'Song categories'
        ordering = ('id',)
        unique_together = (('song', 'category'),)


@receiver([post_save, post_delete], sender=Song)
def trigger_pusher_song(sender, instance, created=None, **kwargs):
    model_trigger(instance, created)


@receiver([post_save, post_delete], sender=SongCategory)
def trigger_pusher_song_category(sender, instance, created=None, **kwargs):
    model_trigger(instance, created)
