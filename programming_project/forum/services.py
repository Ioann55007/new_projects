from django.conf import settings
from django.db.models import Count, QuerySet, Prefetch

from .models import Category, Topic


class BlogService:

    @staticmethod
    def category_queryset() -> QuerySet[Category]:
        return Category.objects.all()

    @staticmethod
    def get_active_articles() -> QuerySet[Topic]:
        return (Topic.objects
                .select_related('category', 'author')
                )


    @staticmethod
    def is_article_slug_exist(title: str) -> bool:
        return Topic.objects.filter(slug=Topic.get_slug(title)).exists()
