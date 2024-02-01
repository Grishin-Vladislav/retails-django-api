from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Product, CustomUser

USER_MODEL = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=3, max_length=255)
    price = serializers.FloatField()
    open_for_sale = serializers.BooleanField(default=True)
    provider = serializers.ReadOnlyField(source='provider.username')

    def validate_name(self, value):
        try:
            Product.objects.get(name=value,
                                provider=self.context['request'].user)
        except Product.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError(
                'Provider and product name must be unique'
            )
        return value

    class Meta:
        model = Product
        fields = ('name', 'price', 'open_for_sale', 'provider')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    def create(self, validated_data):
        user = USER_MODEL.objects.create_user(**validated_data)
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
                  'email', 'is_provider')


class UserDetailSerializer(UserSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('products',)
