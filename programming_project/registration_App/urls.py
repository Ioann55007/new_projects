from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import TemplateAPIView, register, ContactView

from . import views
app_name = 'registration_App'

router = DefaultRouter()


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
]


urlpatterns += [
    path('simple-signup/1', register, name='register'),
    path('send_email', ContactView.as_view(), name='send_email'),
]
