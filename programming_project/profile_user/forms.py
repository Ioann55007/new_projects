from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import Profile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)



class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(widget=forms.EmailInput)
    avatar = forms.ImageField(widget=forms.FileInput(), required=False)
    password = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'

    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')

