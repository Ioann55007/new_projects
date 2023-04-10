from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from django.views.generic import ListView, DetailView
from requests import request
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from taggit.models import Tag
from . import serializers
from .filters import TopicFilter
from .forms import ContactForm, ReplyForm
from .models import Topic, Category, Reply, Bookmarks, Ip, Viewer
from .services import BlogService
from django.views import View
from . import models


class ViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'delete')
    lookup_field = 'slug'
    permission_classes = (AllowAny,)


class Search(ListView):
    model = Topic
    template_name = 'search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tops = Topic.objects.last()
        context['tops'] = tops
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Topic.objects.filter(
            Q(name__icontains=query) | Q(content__icontains=query)
        )

        return object_list

    def topic_list(request, tag_slug=None):
        reply = Reply.objects.filter(topic=id)

        object_list = Topic.published.all()
        topics = Topic.objects.all().order_by('name')
        categories = Category.objects.all()

        if object_list.likes.filter(id=request.user.id).exists():
            object_list.likes.remove(request.user.id)
        else:
            object_list.likes.add(request.user.id)
        if request.method == 'POST':
            form = ReplyForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.topic = object_list
                form.save()
                return redirect('forum:reply_topic', id)
        else:
            form = ReplyForm()
        tag = None

        topic = Topic.objects.get(id=id)
        bookmarks = Bookmarks.objects.filter(user=request.user, topic=topic)

        if not bookmarks.exists():
            Bookmarks.objects.create(user=request.user, topic=topic, quantity=1)
        elif bookmarks.exists():
            bookmark = bookmarks.first()
            bookmark.quantity += 1
            bookmark.save()

            return redirect('profile_user:userpage', request.user.id)
        elif tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            object_list = object_list.filter(tags__in=[tag])

            return render(request, object_list,

                          'search_results.html',
                          {
                              'bookmarks': bookmarks,
                              'comments': reply,
                              'form': form,
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


class TopicListView(ListView):
    model = Topic
    queryset = Topic.objects.all()
    paginate_by = 2
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tops = Topic.objects.last()
        context['tops'] = tops
        return context


class ByCategory(ListView):
    model = Topic
    context_object_name = 'category'

    def get_queryset(self):
        return Topic.objects.filter(url=self.kwargs['id']).selected_related('category')

    def get_success_url(self):
        return reverse('forum:topic_detail', kwargs={"slug": self.object.slug})


class CountViewerMixin:

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if hasattr(self.object, 'viewers'):
            viewer, created = Viewer.objects.get_or_create(
                ipaddress=None if request.user.is_authenticated else get_client_ip(request, id),
                user=request.user if request.user.is_authenticated else None
            )

            if self.object.viewers.filter(id=viewer.id).count() == 0:
                self.object.viewers.add(viewer)

        return response


class TopicDetailView(CountViewerMixin, DetailView):
    model = Topic
    paginate_by = 2

    queryset = Topic.objects.all()
    slug_field = "id"

    def get_context_data(self, *args, **kwargs):
        liked = False
        if self.object.likes.filter(id=self.request.user.id).exists():
            liked = True
        tops = Topic.objects.last()

        context = super().get_context_data(**kwargs)
        context['topic'] = context.get('object')
        context['liked'] = liked
        context['tops'] = tops
        return context


class CategoryDetailView(DetailView):
    model = Category
    slug_field = "slug"

    def like_topic(request, id):
        if request.method == 'POST':
            topic = Topic.objects.get(id=id)
            if topic.likes.filter(id=request.user.id).exists():
                topic.likes.remove(request.user.id)
            else:
                topic.likes.add(request.user.id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def bookmarks_add(request, topic_id):
        topic = Topic.objects.get(id=topic_id)
        bookmarks = Bookmarks.objects.filter(user=request.user, topic=topic)

        if not bookmarks.exists():
            Bookmarks.objects.create(user=request.user, topic=topic, quantity=1)
        else:
            bookmark = bookmarks.first()
            bookmark.quantity += 1
            bookmark.save()

        return redirect('profile_user:userpage', request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tops = Topic.objects.last()
        context['tops'] = tops
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
        response = super().retrieve(request, **kwargs)
        response.template_name = self.get_template_name()
        return response





def modal_latest_topic(request):
    tops = Topic.objects.last()
    return render(request, 'index.html', {'tops': tops})


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
    return render(request, 'forum/topic_detail.html', {'form': form, 'comments': reply, 'topic': topic,
                                                       })


def comment_delete(request, id):
    reply = Reply.objects.get(id=id)
    if reply.user == request.user:
        reply.is_removed = True
        reply.delete()
    else:
        return HttpResponse("You can not delete other people's commentary!")

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def get_client_ip(request, id):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')  # В REMOTE_ADDR значение айпи пользователя
    return ip




def bookmarks_add(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    bookmarks = Bookmarks.objects.filter(user=request.user, topic=topic)

    if not bookmarks.exists():
        Bookmarks.objects.create(user=request.user, topic=topic, quantity=1)
    else:
        bookmark = bookmarks.first()
        bookmark.quantity += 1
        bookmark.save()

    return redirect('profile_user:userpage', request.user.id)


def bookmarks_remove(request, bookmark_id):
    bookmark = Bookmarks.objects.get(id=bookmark_id)
    bookmark.delete()
    return redirect('profile_user:userpage', request.user.id)

