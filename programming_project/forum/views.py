from django.db.models import Q
from .models import Topic, Category
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from taggit.models import Tag


def Main(request):
    topics = Topic.objects.all().order_by('name')
    return render(request, 'index.html', {'topics': topics})


class Search(ListView):
    model = Topic
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Topic.objects.filter(
            Q(name__icontains=query) | Q(content__icontains=query)
        )

        return object_list


    def topic_list(request, tag_slug=None):
        object_list = Topic.published.all()
        topics = Topic.objects.all().order_by('name')
        categories = Category.objects.all()
        tag = None

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            object_list = object_list.filter(tags__in=[tag])
        return render(request, object_list,
                      'search_results.html',
                      {
                       'topic': topics,
                       'category': categories,
                       'tag': tag})


def topic_view(request, category_id):

    cat = Topic.objects.all()
    context = {
        'cat': cat.filter(category=category_id),
        'category': category_id
    }
    return render(request, 'search_results.html', context)



class SingleTopicPageView(View):
    template_name = 'single-topic.html'

    def get(self, request):
        return render(request, self.template_name)

