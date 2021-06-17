from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


# @receiver(post_save, sender=User)
# def create_user(sender, instance, created, **kwargs):
#     if created:
#         group = Group.objects.get(name='member')
#         instance.group.add(group)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def update_profile(sender, instance, **kwargs):
    instance.profile.save()
