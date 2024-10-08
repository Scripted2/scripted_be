from django.shortcuts import get_object_or_404
from rest_framework import serializers
from comments.models import Comment
from users.serializers import ShortUserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer(read_only=True)
    is_liked_by_current_user = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()  # For nested replies

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'video_id', 'user', 'is_liked_by_current_user', 'like_count', 'created_at', 'updated_at', 'parent', 'replies']
        read_only_fields = ['like_count', 'created_at', 'updated_at', 'user', 'replies']

    def get_is_liked_by_current_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.liked_by.filter(id=request.user.id).exists()
        return False

    def get_replies(self, obj):
        '''
        Serializes the comment replies
        '''
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True, context=self.context).data
