from django.db import models
from rest_framework_jwt.serializers import User

from party.models import Party


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
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ('id',)
