from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import UserSerializer, CustomTokenObtainPairSerializer

from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import CodeSnippet
from .serializers import CodeSnippetSerializer
from scripted_be.utils import generic_like

class SignUpViewSet(viewsets.ViewSet):
    """
    ViewSet for user signup.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for token obtain pair.
    """
    serializer_class = CustomTokenObtainPairSerializer


class CodeSnippetViewSet(viewsets.ViewSet):
    """
    A viewset for viewing, editing, creating, and deleting code snippets.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """
        Retrieve a list of code snippets.
        """
        snippets = CodeSnippet.objects.all()
        serializer = CodeSnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific code snippet by ID.
        """
        snippet = get_object_or_404(CodeSnippet, pk=pk)
        serializer = CodeSnippetSerializer(snippet)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = request.user.id

        # Pass the request context to the serializer
        serializer = CodeSnippetSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        """
        Update an existing code snippet.
        """
        snippet = get_object_or_404(CodeSnippet, pk=pk)
        if snippet.created_by != request.user:
            return Response({'error': 'You do not have permission to edit this snippet'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CodeSnippetSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete a specific code snippet by ID.
        """
        snippet = get_object_or_404(CodeSnippet, pk=pk)
        if snippet.created_by != request.user:
            return Response({'error': 'You do not have permission to delete this snippet'}, status=status.HTTP_403_FORBIDDEN)

        snippet.delete()
        return Response({'message': 'Code snippet deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'], url_path='like')
    def like(self, request, pk=None):
        return generic_like(request, CodeSnippet, pk)