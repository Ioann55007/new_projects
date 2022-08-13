from django.apps import apps
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from rest_framework.reverse import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, UserManager


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password1 = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
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
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='topic_likes', default=None, blank=True)
    created = models.DateField(auto_now=False)
    tags = TaggableManager()
    slug = models.SlugField(max_length=130, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    favourites = models.ManyToManyField(User, related_name='favorite', default=None, blank=True)
    excerpt = models.TextField(null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    def total_likes(self):
        return self.likes.count()

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
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User')


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    file = models.FileField(upload_to='feedback_files/', null=True, blank=True)

    class Meta:
        verbose_name = _('Feedback')

