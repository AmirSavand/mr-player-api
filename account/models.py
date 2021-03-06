from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, blank=True, null=True)
    image = models.URLField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)

    @property
    def name(self):
        if self.display_name:
            return self.display_name
        return self.user.username

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    """
    If a user is created, we create an account for that user
    """
    if created:
        Account.objects.create(user=instance)
