
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .views import Search, topic_view, modal_topic, ForumRulesView, modal_latest_topic, ContactUsView

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
    path('5/contact_us/', views.ContactUsView.as_view(), name='contact_us'),
    path('6/email_send/', views.SendEmailView.as_view(), name='contact_us'),

])
