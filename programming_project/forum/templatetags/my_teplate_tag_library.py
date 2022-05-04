from django import template
from forum.models import Topic

register = template.Library()



@register.simple_tag
def last_topic():
    top = Topic.objects.last()

    return {
        'top': top,
    }
