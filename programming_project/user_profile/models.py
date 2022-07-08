# from django.contrib.auth import get_user_model
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.contrib.auth.models import User
# from django.db import models
# from django.contrib.auth.models import User
# from django.dispatch import receiver #add this
# from django.db.models.signals import post_save

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# User = get_user_model()



class UserProfile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')

    avatar = models.ImageField(upload_to='media/', default='no_image.jpg')

    class Meta:
        verbose_name = 'Profile'

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, created: bool, instance, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.UserProfile.save()






