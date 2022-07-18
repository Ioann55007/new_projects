from .views import avatar_img
from django.urls import path
from . import views

app_name = 'profile_user'

urlpatterns = [
    path('profile_upload', avatar_img, name='avatar'),
    path("user/4", views.userpage, name="userpage"),

]
