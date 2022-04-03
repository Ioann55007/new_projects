from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import Search

app_name = 'forum'

urlpatterns = [
    path('', views.Main, name='main'),
    path('search/', Search.as_view(), name='search_results'),

    path('single-topic/', views.SingleTopicPageView.as_view(), name='single-topic'),
]

