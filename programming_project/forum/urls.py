from django.contrib.auth.decorators import login_required
from django.db import router
from django.urls import path, include
from django.conf import settings

from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from django.contrib.auth.decorators import login_required

from .views import Search, topic_view, modal_topic, modal_latest_topic, send_email, TeamView, \
    like_topic, like_reply, bookmarks_add, bookmarks_remove


app_name = 'forum'

urlpatterns = format_suffix_patterns([
    path('', views.TopicListView.as_view(), name='main'),
    path('search/', Search.as_view(), name='search_results'),
    path('search/<category_id>/', topic_view, name='topic_view'),
    path('<slug:slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('r<slug:slug>/<category_id>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path("list/<int:id>", views.TopicViewSet.as_view({'get': 'list'})),
    path("<int:pk>/", views.TopicViewSet.as_view({'get': 'retrieve'})),
    path('1/new_topics/', modal_topic, name='modal_topic'),
    path('2/latest_topic/', modal_latest_topic, name='modal_latest_topic'),
    path('3/forum_rules/', views.ForumRulesView.as_view(), name='forum_rules'),
    path('4/about_us/', views.AboutUsView.as_view(), name='about_us'),
    path('5/email_send/', send_email, name='send_email'),
    path('6/team', TeamView.as_view(), name='the_team'),
    path('like_topic/<int:id>/', like_topic, name='like_topic'),
    path('like_reply/<int:id>/', like_reply, name='like_reply'),
    path('reply/<int:pk>', views.reply_topic, name='reply_topic'),
    path('delete-reply/<int:id>', views.comment_delete, name='delete_reply'),
    path('bookmarks/add/<int:topic_id>/', bookmarks_add, name='bookmarks_add'),
    path('bookmarks/<int:bookmark_id>/', bookmarks_remove, name='bookmarks_remove'),

])




