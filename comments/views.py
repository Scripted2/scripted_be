from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers import CommentSerializer


class CommentView(viewsets.ViewSet):
    """
    Comment view to list, create, retrieve and delete comments.
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='like')
    def like(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user in comment.liked_by.all():
            comment.liked_by.remove(user)
            comment.like_count -= 1
            message = 'Unlike'
        else:
            comment.liked_by.add(user)
            comment.like_count += 1
            message = 'Like'

        comment.save()

        return Response({
            'message': message,
            'like_count': comment.like_count
        }, status=status.HTTP_200_OK)
