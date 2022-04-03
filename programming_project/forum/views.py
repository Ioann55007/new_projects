from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import Topic


def Main(request):
    topics = Topic.objects.all().order_by('name')
    return render(request, 'index.html', {'topics': topics})


class Search(ListView):
    model = Topic
    template_name = 'search_results.html'

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        object_list = Topic.objects.filter(
            Q(name__icontains=query) | Q(content__icontains=query)
        )
        return object_list


class SingleTopicPageView(View):
    template_name = 'single-topic.html'

    def get(self, request):
        return render(request, self.template_name)
