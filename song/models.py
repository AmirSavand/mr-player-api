from django.db import models
from rest_framework_jwt.serializers import User


class SongParty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.SlugField(max_length=16, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else self.key

    class Meta:
        verbose_name_plural = 'Song parties'


class Song(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    party = models.ForeignKey(SongParty, on_delete=models.CASCADE)
    source = models.URLField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source
