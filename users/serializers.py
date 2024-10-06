from rest_framework import serializers

from users.models import User, CodeSnippet, Category


class UserSerializer(serializers.ModelSerializer):
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
        favorite_categories_data = validated_data.pop('favorite_categories')
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        if favorite_categories_data:
            user.favorite_categories.set(favorite_categories_data)
        return user


class CodeSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnippet
        fields = ('title', 'code', 'language', 'created_by', 'created_at', 'updated_at')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name'
