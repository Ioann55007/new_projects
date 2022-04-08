from django import template

from forum.models import Category
from taggit.models import Tag

register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.simple_tag()
def get_tags():
    """Вывод всех тегов"""
    return Tag.objects.all()