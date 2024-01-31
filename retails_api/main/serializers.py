from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Product, CustomUser

USER_MODEL = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    provider = serializers.ReadOnlyField(source='provider.username')

    class Meta:
        model = Product
        fields = ('name', 'price', 'stock', 'provider')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    products = serializers.StringRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        user = USER_MODEL.objects.create(**validated_data)
        return user

    def validate_email(self, value):
        if USER_MODEL.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'User with this email already exists'
            )
        return value

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password',
                  'email', 'products', 'is_provider')
