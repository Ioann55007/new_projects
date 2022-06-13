import re
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import LazyObject
from django.utils.http import url_has_allowed_host_and_scheme, quote_etag
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, check_for_language
)
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from taggit.models import Tag

from . import serializers
from .filters import TopicFilter
from .forms import ContactForm
from .models import Topic, Category

from .services import BlogService
from main_site import settings

import json

from django.http import HttpResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType





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
    tops = Topic.objects.order_by('-id')[0:1]
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


def lang(request, lang_code):
    next = request.POST.get('next', request.GET.get('next'))
    if (next or not request.headers.get('x-requested-with')) and not url_has_allowed_host_and_scheme(url=next,
                                                                                                     allowed_hosts=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if next:
            next = quote_etag(next)  # HTTP_REFERER may be encoded.
        if not url_has_allowed_host_and_scheme(url=next, allowed_hosts=request.get_host()):
            next = '/'
    response = HttpResponseRedirect(next) if next else HttpResponse(status=204)

    if lang_code and check_for_language(lang_code):
        if next:
            for code_tuple in settings.LANGUAGES:
                settings_lang_code = "/" + code_tuple[0]
                parsed = urlsplit(next)
                if parsed.path.startswith(settings_lang_code):
                    path = re.sub('^' + settings_lang_code, '', parsed.path)
                    next = urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))
            response = HttpResponseRedirect(next)
        if hasattr(request, 'session'):
            request.session[LANGUAGE_SESSION_KEY] = lang_code
        else:
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
            )
    return response


def like_topic(request, id):
    if request.method == 'POST':
        topic = Topic.objects.get(id=id)
        if topic.likes.filter(id=request.user.id).exists():
            topic.likes.remove(request.user.id)
        else:
            topic.likes.add(request.user.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

