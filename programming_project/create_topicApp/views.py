import os

from django.shortcuts import render, redirect
from django.views import View

import sys

from .forms import TopicForm

sys.path.append(os.path.abspath('..'))


class CreateTopicView(View):
    template_name = 'create_top.html'

    def get(self, request):
        return render(request, 'create_top.html')



def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect('forum:main')


    else:
        form = TopicForm()
    return render(request, 'topic_create_form.html', {'form': form})






