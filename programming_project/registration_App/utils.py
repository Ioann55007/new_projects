
from requests import get
from .decorators import request_shell


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









