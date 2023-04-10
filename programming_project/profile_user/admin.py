
from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Пользователи"""
    list_display = ("user", "id", 'avatar')
    list_display_links = ("user",)
