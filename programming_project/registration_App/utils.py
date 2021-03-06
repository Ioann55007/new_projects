from email.message import EmailMessage
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from requests import get

from .adapter import AccountAdapter
from .decorators import request_shell


def get_activate_key(user) -> str:
    email_address = EmailAddress.objects.get(user=user)
    email_confirmation = EmailConfirmationHMAC(email_address)
    path = "registration_App:account_verification"
    return AccountAdapter.get_confirmation_url(email_confirmation, path)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@request_shell
def captcha_request(url, params):
    return get(url, params=params, verify=True)









