import json

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from party.models import Party
from playsem.pusher import model_trigger
from song.models import Song


class Dj(models.Model):
    """
    The "time" is the time of the song that's playing.
    The "when" is the time that the "time" was sent by the DJ.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, db_index=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    when = models.TimeField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{user} is a DJ of {party} and playing {song}'.format(
            user=self.user, party=self.party, song=self.song
        )

    class Meta:
        verbose_name = 'DJ'
        verbose_name_plural = 'DJs'
        unique_together = (('user', 'party',),)


class DjUser(models.Model):
    dj = models.ForeignKey(Dj, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)

    @property
    def party(self) -> Party:
        return self.dj.party

    def __str__(self):
        return '{user} is listening to {dj_user} from {party}'.format(
            user=self.user, dj_user=self.dj.user, party=self.party
        )

    class Meta:
        verbose_name = 'DJ user'
        verbose_name_plural = 'DJ users'
        unique_together = (('dj', 'user',),)


@receiver([post_save, post_delete], sender=Dj)
def trigger_pusher_dj(sender, instance: Dj, created=None, **kwargs):
    """
    Trigger pusher when someone becomes DJ or stops being a DJ
    """
    data = {
        'id': instance.pk,
        'user': instance.user.pk,
        'party': str(instance.party.pk),
        'song': instance.song.pk if instance.song else None,
        'time': str(instance.time) if instance.time else None,
        'data': str(instance.date),
    }
    model_trigger(instance, created, data=json.dumps(data))


@receiver([post_save, post_delete], sender=DjUser)
def trigger_pusher_dj_user(sender, instance: DjUser, created=None, **kwargs):
    """
    Trigger pusher when someone connects to a DJ or disconnects from a DJ
    """
    data = {
        'id': instance.pk,
        'dj': instance.dj.pk,
        'user': instance.user.pk,
    }
    model_trigger(instance, created, data=json.dumps(data))
