from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from category.models import Category
from category.serializer import CategorySerializer


class CategoriesViewSet(viewsets.ViewSet):
    """
    ViewSet for categories.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
