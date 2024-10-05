from django.urls import path
from .views import filtered_video_list_view

urlpatterns = [
    path('filtered-videos/', filtered_video_list_view, name='filtered_video_list'),
]