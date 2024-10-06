# serializers.py
from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ['title', 'description', 'view_count', 'like_count', 'duration', 'url', 'created_at', 'user']
