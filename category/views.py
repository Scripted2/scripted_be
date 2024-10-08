from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from category.models import Category
from category.serializer import CategorySerializer


# Create your views here.
class CategoriesViewSet(viewsets.ViewSet):
    """
    ViewSet for categories.
    """

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
