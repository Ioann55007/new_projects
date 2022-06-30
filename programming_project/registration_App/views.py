from django.contrib import messages
from django.views.generic import CreateView
from .tasks import send_inf_email
from .forms import UserRegisterForm
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
import logging
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import logout as django_logout
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth import views as auth_views
from dj_rest_auth.registration.views import (
    VerifyEmailView as _VerifyEmailView,
)
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny

from . import serializers
from .models import Contact
from .services import full_logout, send

logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')

        else:
            messages.error(request, 'Ошибка при регистрации !')
    else:
        form = UserRegisterForm()
    return render(request, 'simple-signup.html', {"form": form})


class ContactView(CreateView):
    model = Contact
    form_class = UserRegisterForm
    success_url = '/'
    template_name = 'simple-signup.html'

    def form_valid(self, form):
        form.save()
        # send(form.instance.email)
        send_inf_email.delay(form.instance.email)
        return super().form_valid(form)



class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer





class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    serializer_class = serializers.PasswordResetConfirmSerializer


class VerifyEmailView(_VerifyEmailView):

    def get_serializer(self, *args, **kwargs):
        return serializers.VerifyEmailSerializer(*args, **kwargs)


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
