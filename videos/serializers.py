# serializers.py
from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    """
    Video serializer to serialize video data.
    """

    class Meta:
        model = Video
        fields = ['title', 'description', 'view_count', 'like_count', 'duration', 'url', 'created_at']
        read_only_fields = ['user']
