from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    """
    Video serializer to serialize video data, including like functionality.
    """
    duration = serializers.FloatField(required=False, allow_null=True, write_only=False)
    user = UserSerializer(read_only=True)
    is_liked_by_current_user = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['title', 'description', 'view_count', 'like_count', 'duration', 'video_file',
                  'created_at', 'updated_at', 'file_hash', 'user', 'is_liked_by_current_user']
        read_only_fields = ['view_count', 'like_count', 'is_liked', 'is_liked_by_current_user']

    def create(self, validated_data):
        user = self.context['request'].user
        instance = Video.objects.create(user=user, **validated_data)
        return instance

    def get_is_liked_by_current_user(self, obj):
        """
        Returns whether the current user has liked the video.
        """
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.liked_by.filter(id=request.user.id).exists()
        return False
