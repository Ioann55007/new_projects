from django.apps import apps
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.signals import setting_changed
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.core.signals import setting_changed
from django.dispatch import receiver




class Profile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')

     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

     avatar = models.ImageField(default='media/no_image.jpg', null=True, blank=True)

     @receiver(post_save, sender=User)
     def create_profile(sender, instance, created, **kwargs):
          if created:
             Profile.objects.create(user=instance)

    # def post_save_receiver(sender, instance, created, **kwargs):
    #     pass
    #
    #     post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)



