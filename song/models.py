from django.db import models
from rest_framework_jwt.serializers import User

from party.models import Party, PartyCategory


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
