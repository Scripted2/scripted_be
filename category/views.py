from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from category.models import Category
from category.serializer import CategorySerializer


class CategoriesViewSet(viewsets.ViewSet):
    """
    ViewSet for categories.
    """
    authentication_classes = []

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdminUser]
        self.permission_classes = [AllowAny]
        return super().get_permissions()

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if Category.objects.filter(name=request.data['name']).exists():
            return Response({'error': 'Category with the same name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
