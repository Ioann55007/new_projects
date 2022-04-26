from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from rest_framework.reverse import reverse_lazy


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
    content = models.TextField()
    tags = TaggableManager()
    # url = models.SlugField(max_length=130, unique=True)
    slug = models.SlugField(max_length=130, unique=True)

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
        return self. author_name


# class Views(models.Model):
#     topic = models.ForeignKey(Topic, related_name='topic_views_set', on_delete=models.SET_NULL, null=True)


class Created(models.Model):
    topic = models.ForeignKey(Topic, related_name='topic_created_set', on_delete=models.SET_NULL, null=True)


class User(models.Model):
    name = models.CharField(max_length=12)
    image = models.ImageField(upload_to='media/', default='no_image.jpg')