from .views import avatar_img
from django.urls import path
from . import views

app_name = 'profile_user'

urlpatterns = [
    path('profile_upload', avatar_img, name='avatar'),
    path("user/<int:id>/", views.userpage, name="userpage"),
    path('delete-profile/<int:pk>/', views.DeleteProfile.as_view(), name="delete-profile"),
    path('edit/<int:pk>/', views.ProfileUpdate.as_view(), name='edit'),
    path('profile', views.profile, name='profile'),

]
