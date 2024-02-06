from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Product, CustomUser

USER_MODEL = get_user_model()


class ListProductsSerializer(serializers.ListSerializer):
    def validate(self, data):
        names = [item['name'] for item in data]
        unique_names = set()
        duplicates = set()

        for name in names:
            if name in unique_names:
                duplicates.add(name)
            else:
                unique_names.add(name)

        if duplicates:
            error_message = f"These products are duplicated in your list: " \
                            f"{', '.join(duplicates)}"
            raise serializers.ValidationError(
                {"duplicated products": error_message})

        return data


class ProductSerializer(serializers.ModelSerializer):
    provider = serializers.ReadOnlyField(source='provider.username')

    def validate_name(self, value):
        try:
            Product.objects.get(
                name=value, provider=self.context['request'].user
            )
        except Product.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError(
                f'You already have a product with this name - {value}'
            )
        return value

    class Meta:
        model = Product
        fields = ('name', 'price', 'open_for_sale', 'provider')
        list_serializer_class = ListProductsSerializer


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
