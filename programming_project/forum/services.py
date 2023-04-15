from django.db.models import QuerySet

from .models import Category, Topic


class BlogService:
    @staticmethod
    def category_queryset() -> QuerySet[Category]:
        return Category.objects.all()

    @staticmethod
    def get_active_topics() -> QuerySet[Topic]:
        return (Topic.objects
                .select_related('category'))

    @staticmethod
    def is_topic_slug_exist(name: str) -> bool:
        return Topic.objects.filter(slug=Topic.slug(name)).exists()


from django.contrib.auth import get_user_model

User = get_user_model()




