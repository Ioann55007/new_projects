from django.db import router
from django.urls import path
from django.conf import settings

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from . import views
from .views import Search, topic_view, modal_topic, ForumRulesView, modal_latest_topic, send_email

app_name = 'forum'

router = DefaultRouter()


urlpatterns = format_suffix_patterns([
    path('', views.TopicListView.as_view(), name='main'),
    path('single-topic/', views.SingleTopicPageView.as_view(), name='single-topic'),
    path('search/', Search.as_view(), name='search_results'),
    path('search/<category_id>/', topic_view, name='topic_view'),
    path('<slug:slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('r<slug:slug>/<category_id>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path("list/1/", views.TopicViewSet.as_view({'get': 'list'})),
    path("<int:pk>/", views.TopicViewSet.as_view({'get': 'retrieve'})),
    path('1/new_topics/', modal_topic, name='modal_topic'),
    path('2/latest_topic/', modal_latest_topic, name='modal_latest_topic'),
    path('3/forum_rules/', views.ForumRulesView.as_view(), name='forum_rules'),
    path('4/about_us/', views.AboutUsView.as_view(), name='about_us'),
    path('5/email_send/', send_email, name='send_email'),
])
