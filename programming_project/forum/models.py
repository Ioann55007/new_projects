import self as self
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=17)
    author = models.CharField(max_length=9)
    created = models.DateField(auto_now=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Topic(models.Model):
    name = models.CharField(max_length=30)
    category = models.ManyToManyField(Category, related_name='topic_set', through='ThroughModel')
    author = models.CharField(max_length=9)
    created = models.DateField(auto_now=False)
    # views = models.ForeignKey('Views', related_name='views_set', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.name


class ThroughModel(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, related_name='topic_set', on_delete=models.SET_NULL, null=True)


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
    image = models.ImageField(upload_to='images/')
