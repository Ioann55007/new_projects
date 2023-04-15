"""
Django settings for main_site project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from os import environ

BASE_DIR = Path(__file__).resolve().parent.parent



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'forum.apps.ForumConfig',
    'create_topicApp.apps.CreateTopicappConfig',
    'registration_App.apps.RegistrationAppConfig',
    'taggit',
    'django.contrib.humanize',
    'drf_yasg',
    'rest_framework.authtoken',
    'profile_user.apps.ProfileUserConfig',
    'crispy_forms',
    'django_social_share',
    'bootstrap3',
    'bootstrap4',
    'crispy_bootstrap4'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main_site.wsgi.application'



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ('ru', 'Russian'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

THIRD_PARTY_APPS = [
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework_simplejwt.token_blacklist',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'corsheaders',

]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'microservice_request.permissions.HasApiKeyOrIsAuthenticated',
        'rest_framework.permissions.IsAuthenticated',

    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',

        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',

    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
ENABLE_RENDERING = int(os.environ.get('ENABLE_RENDERING', 1))

if ENABLE_RENDERING:
    """ For build CMS using DRF """
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    )

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'username',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v7.0',
        'APP': {
            'client_id': environ.get('FACEBOOK_CLIENT_ID'),
            'secret': environ.get('FACEBOOK_SECRET_KEY'),

        }
    }
}

INSTALLED_APPS += THIRD_PARTY_APPS



JWT_AUTH_REFRESH_COOKIE = 'refresh'
JWT_AUTH_COOKIE = 'jwt-auth'
REST_USE_JWT = True
REST_SESSION_LOGIN = False
CORS_ALLOW_CREDENTIALS = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': environ.get('SECRET_KEY'),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=2),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'description': 'Value example: Bearer ******************',
            'in': 'header'
        },
        'Api-Key': {
            'type': 'apiKey',
            'name': 'Authorization',
            'description': 'Value example: <API_KEY_HEADER> <API_KEY>',
            'in': 'header'
        },
        'Language': {
            'type': 'apiKey',
            'name': 'Accept-Language',
            'in': 'header',
            'description': 'Your language code. Example: ua,ru,en',
            'default': 'en'
        },
    },
    'USE_SESSION_AUTH': True,
    'JSON_EDITOR': False,
    'LOGOUT_URL': 'rest_framework:logout',
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_PROFILE_MODULE = 'profile_user.UserProfile'

AUTH_USER_MODEL = 'forum.User'



try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *


