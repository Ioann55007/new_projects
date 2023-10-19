import os

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

import sys

from .forms import TopicForm
from forum.models import Topic

sys.path.append(os.path.abspath('..'))


class CreateTopicView(View):
    template_name = 'create_top.html'

    def get(self, request):
        return render(request, 'create_top.html')


def create_topic(request):
    tops = Topic.objects.last()

    if request.method == 'POST':
        form = TopicForm(request.POST, request.user)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('forum:main')
    else:
        form = TopicForm()
    return render(request, 'topic_create_form.html', {'form': form, 'tops': tops})
