from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, CodeSnippet, Category


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model.
    """
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'favorite_categories')
        extra_kwargs = {
            'password': {'write_only': True},
            'favorite_categories': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Password fields do not match'})
        return attrs

    def create(self, validated_data):
        favorite_categories_data = validated_data.pop('favorite_categories', None)
        validated_data.pop('confirm_password', None)
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if favorite_categories_data:
                user.favorite_categories.set(favorite_categories_data)
        return user


class CodeSnippetSerializer(serializers.ModelSerializer):
    """
    Serializer for code snippet model.
    """

    class Meta:
        model = CodeSnippet
        fields = ('title', 'code', 'language', 'created_by', 'created_at', 'updated_at')


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for category model.
    """

    class Meta:
        model = Category
        fields = '__all__'


class LoginProfileSerializer(UserSerializer):
    """
    Serializer for user profile.
    """

    def to_representation(self, instance):
        return serializers.ModelSerializer.to_representation(self, instance)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token obtain pair serializer.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = LoginProfileSerializer(self.user).data
        return data
