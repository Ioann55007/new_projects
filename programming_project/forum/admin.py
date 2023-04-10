
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Category, Topic, Reply, Viewer
from django.contrib import admin
from . import models


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("name", "id", 'slug')
    list_display_links = ("name",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Темы"""
    list_display = ("name", 'tag_list', 'slug')
    search_fields = ('name', 'category', 'likes', 'created')
    prepopulated_fields = {'slug': ('name',)}





@admin.register(Reply)
class RepliesAdmin(admin.ModelAdmin):
    """Ответы"""
    list_display = ('author', 'created', 'parent', 'topic', 'content')


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['username', 'email'
                    ]


@admin.register(Viewer)
class ViewerAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(models.User, UserAdmin)




