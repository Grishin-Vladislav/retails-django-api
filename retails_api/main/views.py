from rest_framework import generics, permissions

from .permissions import IsOwnerOrReadOnly, IsProviderOrReadOnly
from .serializers import ProductSerializer, UserSerializer, \
    UserDetailSerializer
from .models import Product, CustomUser


class ProductView(generics.ListCreateAPIView):
    """
    GET api/products/
    POST api/products/ (auth required)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly, IsProviderOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)


class UserList(generics.ListCreateAPIView):
    """
    GET api/users/
    POST api/users/
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    GET api/users/1
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
