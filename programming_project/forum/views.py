from django.db.models import Q, QuerySet


from .models import Topic, Category
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from taggit.models import Tag
from rest_framework.viewsets import ModelViewSet
from . import serializers

#
# def Main(request):
#     topics = Topic.objects.all().order_by('name')
#     return render(request, 'index.html', {'topics': topics})

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


class TopicListView(ListView):
    model = Topic
    queryset = Topic.objects.all()
    template_name = 'index.html'


class TopicDetailView(DetailView):
    model = Topic
    queryset = Topic.objects.all()
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context





# class ViewSet(ModelViewSet):
#     http_method_names = ('get', 'post', 'put', 'delete')
#     lookup_field = 'name'


# class TopicViewSet(ViewSet):

    # def get_queryset(self):
    #     return Topic.objects.all()
    #
    # def topic_detail(request):
    #     topics = Topic.objects.all().order_by('name')
    #     topic_author = Topic.objects.all()
    #     categories = Category.objects.all()

        # return render(request,
        #               'topic_detail.html',
        #               {
        #                   'topics': topics,
        #                   'category': categories,
        #                   'topic_author': topic_author,
        #               })

    # def get_template_name(self):
    #     if self.action == 'retrieve':
    #         return 'topic_detail.html'
    #
    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return serializers.TopicUnSerializer
    #
    # def retrieve(self, request, **kwargs):
    #     response = super().retrieve(request, **kwargs)
    #     response.template_name = self.get_template_name()
    #     return response




