from django import forms
from django.forms import ModelForm

from .models import Reply


class ContactForm(forms.Form):
    email = forms.EmailField(label='Введите вашу почту', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

