from django.contrib.auth.models import User
from django.db import models


class LikeKind:
    USER = 0
    PARTY = 1
    CATEGORY = 2
    SONG = 3


class Like(models.Model):
    LIKE_KIND_CHOICES = (
        (LikeKind.USER, 'User'),
        (LikeKind.PARTY, 'Party'),
        (LikeKind.CATEGORY, 'Category'),
        (LikeKind.SONG, 'Song'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.IntegerField(choices=LIKE_KIND_CHOICES)
    like = models.ForeignObject()
    date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return '{user} likes a {kind} with PK of {pk}'.format(user=self.user, self.kind)

    class Meta:
        ordering = ('id',)
