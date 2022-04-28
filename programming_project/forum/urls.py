
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .views import Search, topic_view

app_name = 'forum'

router = DefaultRouter()
# router.register('categories', views.CategoryViewSet, basename='categories')
router.register('posts', views.TopicViewSet, basename='post')


urlpatterns = format_suffix_patterns([
    path('', views.TopicListView.as_view(), name='main'),
    path('single-topic/', views.SingleTopicPageView.as_view(), name='single-topic'),
    path('search/', Search.as_view(), name='search_results'),
    path('search/<category_id>/', topic_view, name='topic_view'),
    path('<slug:slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('r<slug:slug>/<category_id>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path("topic/12/", views.TopicViewSet.as_view({'get': 'list'})),

])

# urlpatterns = format_suffix_patterns([
#     path("movie/", views.MovieViewSet.as_view({'get': 'list'})),
# ])
