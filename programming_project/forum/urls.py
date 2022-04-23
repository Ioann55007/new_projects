import category
from PIL.XVThumbImagePlugin import r
from django.conf import settings
from django.conf.urls.static import static
from django.template.defaulttags import url
from django.urls import path
from . import views
from .views import Search, topic_view

app_name = 'forum'

urlpatterns = [
    path('single-topic/', views.SingleTopicPageView.as_view(), name='single-topic'),
    path('', views.TopicListView.as_view(), name='main'),
    path('search/', Search.as_view(), name='search_results'),
    path('search/<category_id>/', topic_view, name='topic_view'),
    path('<slug:slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path(r'<slug:slug>/<category_id>/', views.CategoryDetailView.as_view(), name='category_detail'),
    # path('category/<slug:slug>/', views.ByCategory.as_view(), name='category'),
    # path('<category_id>/', views.topicInCategory, name='category'),
]
