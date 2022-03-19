from django.contrib import admin

from .models import Category, Topic, Replies,  User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("name", "id")
    list_display_links = ("name",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Темы"""
    list_display = ('views',)

    def display_category(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([category.name for category in self.category.all()[:3]])

    display_category.short_description = 'Category'

    def display_author(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([author.name for author in self.author.all()])

    display_category.short_description = 'Author'


@admin.register(Replies)
class RepliesAdmin(admin.ModelAdmin):
    """Ответы"""
    list_display = ('author_name', 'created')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Просмотры"""
    list_display = ('name', 'image')
