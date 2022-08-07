from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Category, Topic, Replies, User


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
    list_display = ("name", 'category', 'tag_list', 'slug')
    fields = ('category', 'name',  'author',  'content', 'created', 'tags', 'slug', 'likes', 'status')
    search_fields = ('name', 'category', 'likes')


@admin.register(Replies)
class RepliesAdmin(admin.ModelAdmin):
    """Ответы"""
    list_display = ('author_name', 'created')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Пользователи"""
    list_display = ('name', 'image')
    search_fields = ('name',)







