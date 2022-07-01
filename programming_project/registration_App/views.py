from datetime import datetime
from email.message import EmailMessage
from profile import Profile
from random import random

from coreapi.compat import force_text
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView
from django_registration.forms import RegistrationForm
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
import logging
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import logout as django_logout, authenticate, login, get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth import views as auth_views
from dj_rest_auth.registration.views import (
    VerifyEmailView as _VerifyEmailView,
)
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny

from . import serializers
from .forms import  SignupForm
from .models import Contact
from .services import full_logout, send
from .token import account_activation_token

logger = logging.getLogger(__name__)


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрировались!')
#
#         else:
#             messages.error(request, 'Ошибка при регистрации !')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'simple-signup.html', {"form": form})


# class ContactView(CreateView):
#     model = Contact
#     form_class = UserRegisterForm
#     success_url = '/'
#     template_name = 'simple-signup.html'
#
#     def form_valid(self, form):
#         form.save()
#         send(form.instance.email)
#         return super().form_valid(form)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Пожалуйста перейди по ссылке и заверши регистрацию')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Спасибо за подтверждение электронной почты. Теперь вы можете войти в свою учетную запись.')
    else:
        return HttpResponse('Activation link is invalid!')



class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer







class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        response = full_logout(request)
        return response


class TemplateAPIView(APIView):
    """ Help to build CMS System using DRF, JWT and Cookies
        path('some-path/', TemplateAPIView.as_view(template_name='template.html'))
    """
    permission_classes = (AllowAny,)
    template_name = 'verification_sent.html'

    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    def get(self, request, *args, **kwargs):
        return Response
