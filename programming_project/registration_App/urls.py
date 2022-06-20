from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import TemplateAPIView

from . import views
app_name = 'registration_App'

router = DefaultRouter()


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
]


urlpatterns += [
    path('simple-signup/1', views.SimpleSignupView.as_view(), name='simple-signup'),
]


urlpatterns += [
    path('sign-in/', views.LoginView.as_view(), name='api_login'),
    path('sign-up/22', views.SignUpView.as_view(), name='api_sign_up'),
    path('sign-up/verify/', views.VerifyEmailView.as_view(), name='api_sign_up_verify'),
    path('password/reset/', views.PasswordResetView.as_view(), name='api_forgot_password'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='reset_confirm'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls


if settings.ENABLE_RENDERING:
    urlpatterns += [
        path('login/', TemplateAPIView.as_view(template_name='login.html'), name='login'),
        path('email-sent/verify/', TemplateAPIView.as_view(template_name='verification_sent.html'),
             name='verify_email_sent'),
        path('email-sent/reset/', TemplateAPIView.as_view(template_name='reset_password_sent.html'),
             name='reset_email_sent'),
        path('password-reset/<uidb64>/<token>/',
             TemplateAPIView.as_view(template_name='reset_password_confirm.html'), name='pass_reset_confirm'),
        path('verify-email/<key>/', TemplateAPIView.as_view(template_name='email_verification.html'),
             name='account_verification'),
    ]



