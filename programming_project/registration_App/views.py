from email.message import EmailMessage

from coreapi.compat import force_text
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
import logging
from django.contrib.auth import get_user_model, logout
from django.views.generic import TemplateView

from .forms import SignupForm, UserLoginForm
from .models import EmailVerification
from .token import account_activation_token
from django.contrib.auth import login

from forum.models import User

logger = logging.getLogger(__name__)


class EmailVirificationView(TemplateView):
    template_name = "email_verification.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "email confirmation"
        return context

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verify_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return redirect('index')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подтвердите регистрацию по почте')
            return redirect('registration_App:login')
    else:
        form = SignupForm()
    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'signup.html', context)


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


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('forum:main')
    else:
        form = UserLoginForm
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('registration_App:login')
