from .filters import TopicFilter
from django.db.models import Q
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponseRedirect

from . import serializers
from .models import Topic, Category
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from taggit.models import Tag

from .serializers import TopicListSerializers, TopicDetailSerializer
from .services import BlogService


class ViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'delete')
    lookup_field = 'slug'
    permission_classes = (AllowAny,)


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



class ByCategory(ListView):
    model = Topic
    context_object_name = 'category'

    def get_queryset(self):
        return Topic.objects.filter(url=self.kwargs['id']).selected_related('category')

    def get_success_url(self):
        return reverse('forum:topic_detail', kwargs={"slug": self.object.slug})


class TopicDetailView(DetailView):
    model = Topic
    queryset = Topic.objects.all()
    slug_field = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class CategoryDetailView(DetailView):
    model = Category
    # queryset = Category.objects.all()
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


    def topicInCategory(request, id):
        category = Category.objects.filter().get(id=id)
        topics = category.topic_set.all()
        return render(request, 'forum:category_detail.html', {'category': category,  'topics': topics})


class TopicViewSet(ViewSet):
    filterset_class = TopicFilter

    def get_template_name(self):
        if self.action == 'list':
            return 'index.html'
        elif self.action == 'retrieve':
            return 'forum/topic_detail.html'

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.TopicSerializer
        elif self.action == 'create':
            return serializers.CreatedSerializer

    def get_queryset(self):
        return BlogService.get_active_topics()

    def list(self, request, **kwargs):
        response = super().list(request, **kwargs)
        response.template_name = self.get_template_name()
        return response

    def retrieve(self, request, **kwargs):
        response = super().list(request, **kwargs)
        response.template_name = self.get_template_name()
        return response



def modal_topic(request):
    topic = Topic.objects.order_by('-id')[0:5]
    return render(request,  'modal_new_topics.html', {'topic': topic})

