from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserSerializer, CustomTokenObtainPairSerializer


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
