from rest_framework import serializers

from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for category model.
    """

    class Meta:
        model = Category
        fields = '__all__'
