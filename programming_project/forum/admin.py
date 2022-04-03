from django.contrib import admin
from taggit.admin import TagAdmin

from .models import Category, Topic, Replies, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("name",)
    list_display_links = ("name",)


# @admin.register(Views)
# class ViewsAdmin(admin.ModelAdmin):
#     fields = ('topic',)


# @admin.register(TagAdmin)
# class TopicTagAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     fields = ('name',)



@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Темы"""
    # list_display = ('views',)
    list_display = ("category", 'name', 'tags')
    fields = ('category', 'name',  'author',  'content', 'created', 'tags')



@admin.register(Replies)
class RepliesAdmin(admin.ModelAdmin):
    """Ответы"""
    list_display = ('author_name', 'created')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Пользователи"""
    list_display = ('name', 'image')
