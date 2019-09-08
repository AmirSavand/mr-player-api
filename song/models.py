from django.db import models
from rest_framework_jwt.serializers import User

from party.models import Party, PartyCategory


class SongPlayer:
    YOUTUBE = 0
    SOUNDCLOUD = 1


class Song(models.Model):
    SONG_PLAYER_CHOICES = (
        (SongPlayer.YOUTUBE, 'YouTube'),
        (SongPlayer.SOUNDCLOUD, 'SoundCloud'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    player = models.IntegerField(choices=SONG_PLAYER_CHOICES, default=SongPlayer.YOUTUBE)
    source = models.URLField()
    name = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ('id',)


class SongCategory(models.Model):
    song = models.ForeignKey(Song, related_name='song_category', on_delete=models.CASCADE)
    category = models.ForeignKey(PartyCategory, related_name='song_category', on_delete=models.CASCADE)
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
