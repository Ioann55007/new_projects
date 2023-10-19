from django.core.mail import send_mail, BadHeaderError
from django.db import models
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.utils.timezone import now
from forum.models import User
from django.db.models.signals import post_save

from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _



class Profile(models.Model):
     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_user', verbose_name='User')
     avatar = models.ImageField(User, upload_to='',  default='/no_image.jpg', blank=True)


     class Meta:
         verbose_name = _('Profile')


     @receiver(post_save, sender=User)
     def create_profile(sender, instance, created, **kwargs):
          if created:
             Profile.objects.create(user=instance)




