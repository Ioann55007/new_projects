import re
from urllib.parse import urlsplit, urlunsplit
import datetime
import form as form
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.db.models import OuterRef, Subquery, Exists

# from .models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.functional import LazyObject
from django.utils.http import url_has_allowed_host_and_scheme, quote_etag
# from django.utils.translation import (
#     LANGUAGE_SESSION_KEY, check_for_language
# )
from django.views import View, generic
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from taggit.models import Tag

from . import serializers
from .filters import TopicFilter
from .forms import ContactForm, ReplyForm
from .models import Topic, Category, Bookmark, Reply, Ip

from .services import BlogService
from main_site import settings

import json

from django.http import HttpResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType
from . import models


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

    def get_context_data(self, *args, **kwargs):
        liked = False
        if self.object.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = super().get_context_data(**kwargs)
        context['topic'] = context.get('object')
        context['liked'] = liked
        return context

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip




class CategoryDetailView(DetailView):
    model = Category
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def topicInCategory(request, id):
        category = Category.objects.filter().get(id=id)
        topics = category.topic_set.all()
        return render(request, 'forum:category_detail.html', {'category': category, 'topics': topics})


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
    return render(request, 'modal_new_topics.html', {'topic': topic})


def modal_latest_topic(request):
    # tops = Topic.objects.order_by('-id')[0:1]
    tops = Topic.objects.last()
    return render(request, 'modal_latest_topic.html', {'tops': tops})


class ForumRulesView(View):
    template_name = 'forum_rules.html'

    def get(self, request):
        return render(request, self.template_name)


class AboutUsView(View):
    template_name = 'about_us.html'

    def get(self, request):
        return render(request, self.template_name)


def send_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['email'], form.cleaned_data['content'],
                             'forumprogrammer.site@gmail.com', ['ioann.basic@gmail.com'], fail_silently=False)

            if mail:
                return render(request, 'email/send_email.html')

    else:
        form = ContactForm()
    return render(request, 'email/contact_us.html', {'form': form})


class TeamView(View):
    template_name = 'team/the_team.html'

    def get(self, request):
        return render(request, self.template_name)


def like_topic(request, id):
    if request.method == 'POST':
        topic = Topic.objects.get(id=id)
        if topic.likes.filter(id=request.user.id).exists():
            topic.likes.remove(request.user.id)
        else:
            topic.likes.add(request.user.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def like_reply(request, id):
    if request.method == 'POST':
        reply = Reply.objects.get(id=id)
        if reply.likes.filter(id=request.user.id).exists():
            reply.likes.remove(request.user.id)
        else:
            reply.likes.add(request.user.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class List(LoginRequiredMixin, generic.ListView):
    model = models.Topic

    def get_queryset(self):
        return self.request.user.topic_bookmark.all()


class Create(LoginRequiredMixin, generic.CreateView):
    fields = ['author', 'name', 'content', 'tags', 'id', 'category']
    model = models.Topic
    success_url = reverse_lazy('forum:list_topic_bookmark')

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.user = self.request.user
        topic.save()
        form.save_m2m()
        return super().form_valid(form)


class Update(LoginRequiredMixin, generic.UpdateView):
    fields = ['author', 'name', 'content', 'tags']
    model = models.Topic

    success_url = reverse_lazy('forum:list_topic_bookmark')

    def get_queryset(self):
        return self.request.user.topic_bookmark.all()


class Delete(LoginRequiredMixin, generic.DeleteView):
    model = models.Topic
    success_url = reverse_lazy('forum:list_topic_bookmark')

    def get_queryset(self):
        return self.request.user.topic_bookmark.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_view'] = True
        return context


def reply_topic(request, pk):
    topic = get_object_or_404(Topic, id=pk)
    reply = Reply.objects.filter(topic=pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.topic = topic
            form.save()
            return redirect('forum:reply_topic', pk)
    else:
        form = ReplyForm()
    # return render(request, 'forum/comments.html', {'form': form, 'comments': reply, 'topic': topic})
    return render(request, 'forum/topic_detail.html', {'form': form, 'comments': reply, 'topic': topic})


def to_get_reply(request, id):
    selected_reply = get_object_or_404(Reply, id=id)
    selected_reply.delete()
    return redirect('forum:reply_topic', id)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')  # В REMOTE_ADDR значение айпи пользователя
    return ip




def post_view(request, slug):
    topic = Topic.objects.get(slug=slug)

    ip = get_client_ip(request)

    if Ip.objects.filter(ip=ip).exists():
        topic.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        topic.views.add(Ip.objects.get(ip=ip))

    context = {
        'topic': topic,
    }
    return render(request, 'forum/topic_detail.html', context)



def get_ip(request):
    address=request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip=address.split(',')[0].strip()
    else:
        ip=request.META.get('REMOTE_ADDR')
    return ip
# Создаст функцию которая будет брать ip запроса


def topic(request, slug):
    ask = get_object_or_404(Topic, slug=slug)
    ip = get_ip(request)  # Не забудьте импортировать функцию если она находится в другом месте
    TopicViews.objects.get_or_create(IPAddres=ip, topic=ask)
    return render(request, 'topic.html', {'topic': ask})