from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Category, Topic, Reply, Ip
from django.contrib import admin
from .models import User
from . import models


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("name", "id", 'slug')
    list_display_links = ("name",)


# @admin.register(Views)
# class ViewsAdmin(admin.ModelAdmin):
#     fields = ('topic',)



@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Темы"""
    # list_display = ('views',)
    list_display = ("name", 'tag_list', 'slug')
    search_fields = ('name', 'category', 'likes', 'created')


admin.site.register(Ip)


@admin.register(Reply)
class RepliesAdmin(admin.ModelAdmin):
    """Ответы"""
    list_display = ('author', 'created', 'parent', 'topic', 'content')


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['username', 'email'
                    ]


admin.site.register(models.User, UserAdmin)


@admin.register(models.Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'user']

