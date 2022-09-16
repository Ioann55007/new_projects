import datetime
import uuid
from time import time

import requests
from django.apps import apps
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.sessions.backends import db
from django.utils.timezone import localdate

# Create your models here.
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from rest_framework.reverse import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, UserManager


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(u'date joined', default=timezone.now)
    objects = UserManager()
    avatar = models.ImageField(settings.AUTH_USER_MODEL, default='media/no_image.jpg', blank=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'password', 'avatar']




class Category(models.Model):
    """Категории"""
    name = models.CharField(max_length=170)
    author = models.CharField(max_length=9)
    created = models.DateField(auto_now=False)
    objects = UserManager()
    slug = models.SlugField(max_length=130, unique=True)
    category_image = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Ip(models.Model):
    ip = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        return self.ip


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '_' + str(int(time()))



class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, verbose_name="Category", on_delete=models.SET_NULL, null=True, related_name='topic'
    )
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='topic_likes', default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    slug = models.SlugField(max_length=130, unique=True, default=uuid.uuid1, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='author_set')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='topic_bookmark')
    views = models.ManyToManyField(Ip, related_name="post_views", blank=True)
    count_user = models.ManyToManyField(User, through="CountUser")

    objects = models.Manager()

    def total_views(self):
        return self.views.count()

    def user_count(self):
        return self.count_user.count()

    def __str__(self):
        return self.name


    def d_date(self):
        z = self.created.strptime(str(self.created), '%Y-%m-%d %H:%M:%S.%f+%U:%W')
        r = datetime.datetime.today()
        e = r - z
        return e

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        # return reverse("forum:topic_detail", kwargs={"slug": self.url})
        return reverse_lazy('forum:topic_detail', kwargs={'slug': self.slug})

    def tag_list(self) -> str:
        return u", ".join(o.name for o in self.tags.all())





    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)





    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'






class CountUser(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='count_topic_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='count_user_user')


    class Meta:
        unique_together = [('user', 'topic')]


class Bookmark(models.Model):
    topic = models.ManyToManyField(Topic, related_name='bookmark_topic_bookmark', default=None, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    url = models.URLField('URL')
    description = models.TextField(default='', blank=True)
    title = models.CharField(default='', blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title if self.title else self.url

    class Meta:
        unique_together = [('url', 'user')]


@receiver(post_save, sender=Bookmark)
def fetch_url_title(sender, instance, created, **kwargs):
    if created:
        r = requests.get(instance.url)
        if r.ok:
            text = r.text
            instance.title = text[text.find('<title>')+7:text.find('<title>')][:255]
            instance.save()


class Reply(models.Model):
    author = models.EmailField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='comment_set', blank=True)
    content = models.TextField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_set', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='reply_likes', default=None, blank=True)

    objects = models.Manager()

    def count_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')
        ordering = ('-id',)


    def __str__(self):
        return self.content


    def last_reply(self):
        k = self.topic.topic_set
        ur = k.order_by('-created')[0]
        f = ur.created
        return f


class Created(models.Model):
    topic = models.ForeignKey(Topic, related_name='topic_created_set', on_delete=models.SET_NULL, null=True)


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    file = models.FileField(upload_to='feedback_files/', null=True, blank=True)

    class Meta:
        verbose_name = _('Feedback')

