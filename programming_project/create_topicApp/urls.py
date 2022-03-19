from django.urls import path
from . import views
app_name = 'create_topicApp'

urlpatterns = [
    path('create_top/', views.CreateTopicView.as_view(), name='create_top'),
]
