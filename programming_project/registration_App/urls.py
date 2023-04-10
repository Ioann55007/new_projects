from django.urls import path, re_path
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
# from .views import TemplateAPIView, register, ContactView

from . import views
from .views import signup, user_login, user_logout
from .views import activate

app_name = 'registration_App'

router = DefaultRouter()


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
]



urlpatterns += [

    path('signup_email', signup, name='signup'),
    path('activate//<uidb64>/<token>/',
            activate, name='activate'),
    path('login/1', user_login, name='login'),
    path('logout/1', user_logout, name='logout'),

]
