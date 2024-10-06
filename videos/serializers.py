from rest_framework import serializers
from urllib3 import request

from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    """
    Video serializer to serialize video data.
    """
    duration = serializers.FloatField(required=False, allow_null=True, write_only=False)

    class Meta:
        model = Video
        fields = ['title', 'description', 'view_count', 'like_count', 'is_liked', 'duration', 'url', 'created_at',
                  'updated_at']
        read_only_fields = ['user', 'view_count', 'like_count', 'is_liked']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)