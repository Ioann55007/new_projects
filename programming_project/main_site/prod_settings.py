import os
from datetime import timedelta
from pathlib import Path
from os import environ

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'ZZZZZdjango-insecure-jb#l7g-6d!-(*5o@nxq!mz=y%8512-12q=a#dkvzt&no12-12$@f%1-pny(jZZZZZ'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ioann.basic@gmail.com'
EMAIL_HOST_PASSWORD = 'kbtdkkbivgrnvjtx'

DEFAULT_FROM_EMAIL = environ.get('DEFAULT_FROM_EMAIL', 'ioann.basic@gmail.com')
EMAIL_USE_TLS = True

ALLOWED_HOSTS: list = os.environ.get("DJANGO_ALLOWED_HOSTS", 'localhost,127.0.0.1').split(",")
FRONTEND_SITE = 'http://localhost:8000'
ENABLE_RENDERING = int(os.environ.get('ENABLE_RENDERING', 1))

SUPERUSER_EMAIL = os.environ.get('SUPERUSER_EMAIL', 'admin@gmail.com')
SUPERUSER_PASSWORD = os.environ.get('SUPERUSER_PASSWORD', '1524ok')

DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS: list = os.environ.get("DJANGO_ALLOWED_HOSTS", 'localhost,127.0.0.1').split(",")
ALLOWED_HOSTS += ['3ef3-94-41-3-182.eu.ngrok.io']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'proger_forum',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
