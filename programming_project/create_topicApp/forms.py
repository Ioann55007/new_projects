from django import forms
from django.core.exceptions import ValidationError

from forum.models import Topic, Category, User


# class TopicForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['category'].empty_label = 'Категория не выбрана'
#
#     class Meta:
#         model = Topic
#         fields = ['name', 'slug', 'tags', 'author', 'category', 'content']
#         widgets = {
#            'name': forms.TextInput(attrs={'class': 'form-input'}),
#            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
#         }


class TopicForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    name = forms.CharField(label='Название темы вопроса', widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = forms.SlugField(label='Слаг', widget=forms.TextInput(attrs={'class': 'form-control'}))
    tags = forms.CharField(label='Теги', widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.ModelChoiceField(queryset=User.objects.all(), label='Автор')
    # category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория')
    content = forms.CharField(label='Контент', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))

    class Meta:
        model = Topic
        fields = ['name', 'slug', 'tags', 'author', 'category', 'content']
