from django.urls import path
from . import views
app_name = 'create_topicApp'

urlpatterns = [
    path('12/topic/create/', views.create_topic, name='topic_create_url'),
]
