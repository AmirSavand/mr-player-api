from django.contrib.auth.models import User
from django.db import models

from party.models import Party, PartyCategory
from song.models import Song


class Like(models.Model):
    class Kind(models.IntegerChoices):
        USER = 1
        PARTY = 2
        CATEGORY = 3
        SONG = 4

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.IntegerField(choices=Kind.choices)
    like = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def like_object(self) -> Party:
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