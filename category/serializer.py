from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for category model.
    """

    class Meta:
        model = Category
        fields = '__all__'


