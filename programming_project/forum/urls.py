from django.contrib.auth.decorators import login_required
from django.db import router
from django.urls import path, include
from django.conf import settings

from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from django.contrib.auth.decorators import login_required

from .views import Search, topic_view, modal_topic, ForumRulesView, modal_latest_topic, send_email, TeamView, like_topic

app_name = 'forum'

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
    path('6/team', TeamView.as_view(), name='the_team'),
    path('lang/<lang_code>/', views.lang, name='lang'),
    path('like_topic/<int:id>/', like_topic, name='like_topic'),
    path("11/bookmarks/", views.List.as_view(), name='list_topic_bookmark'),
    path("15/create/", views.Create.as_view(), name='create'),
    path("update/<int:pk>/", views.Update.as_view(), name="update"),
    path("delete/<int:pk>", views.Delete.as_view(), name="delete"),

])
