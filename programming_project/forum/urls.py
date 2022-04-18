from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import Search, topic_view

app_name = 'forum'

urlpatterns = [
    path('', views.TopicListView.as_view(), name='main'),
    path('single-topic/', views.SingleTopicPageView.as_view(), name='single-topic'),
    path('search/', Search.as_view(), name='search_results'),
    path('search/<category_id>/', topic_view, name='topic_view'),
    path('<slug:slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
]

