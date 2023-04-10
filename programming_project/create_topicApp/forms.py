from django import forms
from django.forms import ModelForm, modelform_factory, Textarea

from forum.models import Topic, Category, User
from django.utils.translation import gettext_lazy as _
from rest_framework import request


# class TopicForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['category'].empty_label = 'Категория не выбрана'
#
#     name = forms.CharField(label='Название темы вопроса', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     slug = forms.SlugField(label='Слаг', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     tags = forms.CharField(label='Теги', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     author = forms.ModelChoiceField(queryset=User.objects.all(), label='Автор')
#     content = forms.CharField(label='Контент', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
#
#     class Meta:
#         model = Topic
#         fields = ['name', 'slug', 'tags', 'author', 'category', 'content']

class TopicForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    name = forms.CharField(label='Name question', widget=forms.TextInput(attrs={'size': '100'}))
    tags = forms.CharField(label='Tags', widget=forms.TextInput(attrs={'size': '13'}))
    author = forms.ModelChoiceField(queryset=User.objects.all(), label='Author')
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))




    class Meta:
        model = Topic
        fields = ['name', 'tags', 'author', 'category', 'content']


# class TopicForm(forms.Form):
#     name = forms.CharField(widget=forms.TextInput(attrs={'size': '100'}))
#     slug = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
#     tags = forms.CharField(widget=forms.TextInput(attrs={'size': '13'}))
#     author = forms.CharField(widget=forms.TextInput(attrs={'size': '42'}))
#     categoty = forms.CharField(widget=forms.TextInput(attrs={'size': '42'}))
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))
