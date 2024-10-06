from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Category
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer, CategorySerializer


class SignUpViewSet(viewsets.ViewSet):
    """
    ViewSet for user signup.
    """

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
