from django.db.models import Q
<<<<<<<<< Temporary merge branch 1
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import Topic
=========
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from taggit.models import Tag
>>>>>>>>> Temporary merge branch 2

from .models import Topic

<<<<<<<<< Temporary merge branch 1
def Main(request):
    topics = Topic.objects.all().order_by('name')
    return render(request, 'index.html', {'topics': topics})

=========

def Main(request):
    topics = Topic.objects.all().order_by('name')
    return render(request, 'index.html', {'topics': topics})

>>>>>>>>> Temporary merge branch 2

class Search(ListView):
    model = Topic
    template_name = 'search_results.html'

<<<<<<<<< Temporary merge branch 1
    def get_queryset(self):  # новый
=========
    def get_queryset(self):
>>>>>>>>> Temporary merge branch 2
        query = self.request.GET.get('q')
        object_list = Topic.objects.filter(
            Q(name__icontains=query) | Q(content__icontains=query)
        )
<<<<<<<<< Temporary merge branch 1
        return object_list
=========

        return object_list

    def post_list(request, tag_slug=None):
        object_list = Topic.published.all()
        topics = Topic.objects.all().order_by('name')

        tag = None

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            object_list = object_list.filter(tags__in=[tag])
        return render(request, object_list,
                      'search_results.html',
                      {
                       'topic': topics,
                       'tag': tag})


class SingleTopicPageView(View):
    template_name = 'single-topic.html'

    def get(self, request):
        return render(request, self.template_name)
