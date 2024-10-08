from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from comment.models import Comment
from comment.serializers import CommentSerializer
from scripted_be.utils import generic_like


class CommentView(viewsets.ViewSet):
    """
    Comment view to list, create, retrieve, delete, and reply to comments.
    """

    def list(self, request):
        queryset = Comment.objects.all()
        comment_data = [CommentSerializer(comment, context={'request': request}).data for comment in queryset]
        return Response(comment_data)

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], url_path='reply')
    def reply(self, request, pk=None):
        """
         Reply to a comment (this will be mapped to POST /comment/<comment_id>/reply/)
        """
        parent_comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, parent=parent_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='like')
    def like(self, request, pk=None):
        return generic_like(request, Comment, pk)
