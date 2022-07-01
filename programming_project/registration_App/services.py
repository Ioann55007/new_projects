import re
from django.core.mail import send_mail
from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Tuple

from .decorators import except_shell
from .tasks import send_information_email
from .utils import captcha_request, get_client_ip, get_activate_key

User = get_user_model()


class CeleryService:

    @staticmethod
    def send_password_reset(content: dict, to_email: str):
        content: dict = {
            'subject': _('Password Reset'),
            'html_email_template_name': 'emails/password_reset.html',
            'to_email': to_email,
            'context': content,
        }
        send_information_email.delay(**content)

    @staticmethod
    def send_email_confirm(user):
        content: dict = {
            'subject': _('Please Confirm Your E-mail Address'),
            'html_email_template_name': 'emails/verify_email.html',
            'to_email': user.email,
            'context': {
                'user': user.get_full_name(),
                'activate_url': get_activate_key(user),
            }
        }
        send_information_email.delay(**content)


class AuthAppService:

    @staticmethod
    def is_user_exist(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        re_email = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,30})+$'
        if not re.search(re_email, email):
            return False, _("Entered email address is not valid")
        return True, ''

    @staticmethod
    def validate_captcha(captcha: str, request) -> tuple:
        url = "https://google.com/recaptcha/api/siteverify"
        params = {
            'secret': settings.GOOGLE_CAPTCHA_SECRET_KEY,
            'response': captcha,
            'remoteip': get_client_ip(request)
        }
        response = captcha_request(url=url, params=params)
        data = response.json()
        status = data.get("success", False)
        return status, data

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email: str):
        return User.objects.get(email=email)

    @staticmethod
    def make_user_active(user):
        user.is_active = True
        user.save
        return user


def full_logout(request):
    response = Response({"detail": _("Successfully logged out.")}, status=HTTP_200_OK)
    if cookie_name := getattr(settings, 'JWT_AUTH_COOKIE', None):
        response.delete_cookie(cookie_name)
    refresh_cookie_name = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
    refresh_token = request.COOKIES.get(refresh_cookie_name)
    if refresh_cookie_name:
        response.delete_cookie(refresh_cookie_name)
    if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
        # add refresh token to blacklist
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except KeyError:
            response.data = {"detail": _("Refresh token was not included in request data.")}
            response.status_code = HTTP_401_UNAUTHORIZED
        except (TokenError, AttributeError, TypeError) as error:
            if hasattr(error, 'args'):
                if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                    response.data = {"detail": _(error.args[0])}
                    response.status_code = HTTP_401_UNAUTHORIZED
                else:
                    response.data = {"detail": _("An error has occurred.")}
                    response.status_code = HTTP_500_INTERNAL_SERVER_ERROR

            else:
                response.data = {"detail": _("An error has occurred.")}
                response.status_code = HTTP_500_INTERNAL_SERVER_ERROR

    else:
        message = _(
            "Neither cookies or blacklist are enabled, so the token "
            "has not been deleted server side. Please make sure the token is deleted client side."
        )
        response.data = {"detail": message}
        response.status_code = HTTP_200_OK
    return response


class UserService:

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email):
        return User.objects.get(email=email)

    @staticmethod
    def email_address_prefetch():
        return Prefetch(
            'emailaddress_set', queryset=EmailAddress.objects.filter(primary=True), to_attr='email_address'
        )


def send(user_email):
    send_mail(
        'Вы успешном зарегистрировались',
        'Переходите по ссылке',
        'ioann.basic@gmail.com',
        [user_email],
        fail_silently=False,
    )
