from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    provider = serializers.ReadOnlyField(source='provider.username')

    class Meta:
        model = Product
        fields = ('name', 'price', 'stock', 'provider')


class UserSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'products')
