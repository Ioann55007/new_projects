from django.conf import settings
from django.db import models

# Create your models here.
from django.db import models
from django.db.models import Sum

from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from rest_framework.reverse import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class User(models.Model):
    name = models.CharField(max_length=12)
    image = models.ImageField(upload_to='media/', default='no_image.jpg')


class Category(models.Model):
    """Категории"""
    name = models.CharField(max_length=170)
    author = models.CharField(max_length=9)
    created = models.DateField(auto_now=False)
    objects = models.Manager()
    slug = models.SlugField(max_length=130, unique=True)

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


class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, verbose_name="Category", on_delete=models.SET_NULL, null=True, related_name='topic'
    )
    author = models.CharField(max_length=9)

    created = models.DateField(auto_now=False)
    # views = models.ForeignKey('Views', related_name='views_set', on_delete=models.CASCADE)
    views = models.ManyToManyField("Ip", related_name="topic_views", blank=True)
    content = models.TextField()
    tags = TaggableManager()
    slug = models.SlugField(max_length=130, unique=True)
    likes = models.ManyToManyField(User, related_name='topic_posts')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse("forum:topic_detail", kwargs={"slug": self.url})
        return reverse_lazy('forum:topic_detail', kwargs={'slug': self.slug})

    def tag_list(self) -> str:
        return u", ".join(o.name for o in self.tags.all())

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'


class Replies(models.Model):
    author_name = models.CharField(max_length=10)
    content = models.TextField()
    topic = models.ForeignKey(Topic, related_name='topic_replies_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_set', blank=True, null=True)

    def __str__(self):
        return self.author_name


# class Views(models.Model):
#     # topic = models.ForeignKey(Topic, related_name='topic_views_set', on_delete=models.SET_NULL, null=True)
#     views = models.ManyToManyField("Ip", related_name="post_views", blank=True)


class Created(models.Model):
    topic = models.ForeignKey(Topic, related_name='topic_created_set', on_delete=models.SET_NULL, null=True)


class Ip(models.Model):
    ip = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ip_user')


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    file = models.FileField(upload_to='feedback_files/', null=True, blank=True)

    class Meta:
        verbose_name = _('Feedback')


# class TopicLikes(models.Model):
#     topic_post = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, verbose_name='Публикация в теме')
#     liked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Поставил лайк')
#     like = models.BooleanField('Like', default=False)
#     created = models.DateTimeField('Дата и время', default=timezone.now)
#
#     def __str__(self):
#         return f'{self.liked_by}:{self.topic_post} {self.like}'
#
#     class Meta:
#         verbose_name = 'Topic Like'
#         verbose_name_plural = 'Topic Likes'

# class TopLikes(models.Model):
#     likes = models.ForeignKey(User, blank=True, on_delete=models.SET_NULL, null=True, related_name='likes', verbose_name='Лайк')
#     dislikes = models.ForeignKey(User, blank=True, on_delete=models.SET_NULL, null=True, related_name='dislikes', verbose_name='дизлайк')
#     created = models.DateTimeField('Дата и время', default=timezone.now)


