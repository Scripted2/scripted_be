from rest_framework import serializers
from urllib3 import request

from users.serializers import UserSerializer
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    """
    Video serializer to serialize video data.
    """
    duration = serializers.FloatField(required=False, allow_null=True, write_only=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Video
        fields = ['title', 'description', 'view_count', 'like_count', 'is_liked', 'duration', 'video_file', 'created_at',
                  'updated_at', 'file_hash', 'user']
        read_only_fields = ['view_count', 'like_count', 'is_liked']

    def create(self, validated_data):
        user = self.context['request'].user
        instance = Video.objects.create(user=user, **validated_data)
        return instance
