# serializers.py
from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer): # Added sterializer to make code cleaner
    class Meta:
        model = Video
        fields = ['title', 'description', 'view_count', 'like_count', 'duration', 'url']
