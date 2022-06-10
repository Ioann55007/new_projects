from django import template
from ..models import TopicLikes

register = template.Library()


@register.simple_tag(takes_context=True)
def is_liked(context, topic_post_id):
    request = context['request']
    try:
        topic_likes = TopicLikes.objects.get(topic_post_id=topic_post_id, liked_by=request.user.id).like
    except Exception as e:
        topic_likes = False
    return topic_likes


@register.simple_tag()
def count_likes(topic_post_id):
    return TopicLikes.objects.filter(topic_post_id=topic_post_id, like=True).count()


@register.simple_tag(takes_context=True)
def topic_likes_id(context, topic_post_id):
    request = context['request']
    return TopicLikes.objects.get(topic_post_id=topic_post_id, liked_by=request.user.id).id

