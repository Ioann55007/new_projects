
from allauth.account.adapter import DefaultAccountAdapter

from django.conf import settings

from rest_framework.reverse import reverse_lazy


class AccountAdapter(DefaultAccountAdapter):

    @staticmethod
    def get_confirmation_url(email_confirmation, path):
        url = reverse_lazy(path, args=[email_confirmation.key])
        return settings.FRONTEND_SITE + str(url)

