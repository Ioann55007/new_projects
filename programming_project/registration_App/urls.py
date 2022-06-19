from django.urls import path
from . import views
app_name = 'registration_App'

urlpatterns = [
    path('simple-signup/1', views.SimpleSignupView.as_view(), name='simple-signup'),
]
