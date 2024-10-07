from rest_framework import serializers

from comments.models import Comment
from users.serializers import ShortUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment serializer to serialize comment data.
    """
    user = ShortUserSerializer(read_only=True)
    is_liked_by_current_user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'video_id', 'user', 'is_liked_by_current_user', 'like_count', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        comment = Comment.objects.create(user=user, **validated_data)
        return comment

    def get_is_liked_by_current_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.liked_by.filter(id=request.user.id).exists()
        return False
