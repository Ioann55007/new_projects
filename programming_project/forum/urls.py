
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .views import Search, topic_view, modal_topic

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

])
