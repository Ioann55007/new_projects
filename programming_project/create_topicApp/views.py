import os

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
import sys

from .forms import TopicForm

from forum.models import Topic
from forum.models import Category


sys.path.append(os.path.abspath('..'))


class CreateTopicView(View):
    template_name = 'create_top.html'

    def get(self, request):
        return render(request, 'create_top.html')


# class TopicCreate(View):
#     def get(self, request):
#         form = TopicForm()
#         return render(request, 'topic_create_form.html', context={'form': form})
#
#     def post(self, request):
        # bound_form = TopicForm(request.POST)
        # if bound_form.is_valid():
        #     # new_topic =
        #     bound_form.save()
        #     return redirect('create_topicApp:topic_create_url')
        # return render(request, 'create_top.html', context={'form': bound_form})
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # try:
                # Topic.objects.create(**form.cleaned_data)
            form.save()
            return redirect('forum:main')
            # except:
            #     form.add_error(None, 'Ошибка создание вопроса')

    else:
        form = TopicForm()
    return render(request, 'topic_create_form.html', {'form': form})






