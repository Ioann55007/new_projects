from django import forms
from django.forms import ModelForm, modelform_factory

from .models import Reply, Topic


class ContactForm(forms.Form):
    email = forms.EmailField(label='Введите вашу почту', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))


class ReplyForm(ModelForm):



    content = forms.CharField(label='Контент', widget=forms.Textarea(attrs={'cols': 80, 'rows': 10}))

    class Meta:
        model = Reply
        fields = ['content']


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', 'category', 'content')
