from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken

from .permissions import IsOwnerOrReadOnly, IsProviderOrReadOnly
from .serializers import ProductSerializer, UserSerializer, \
    UserDetailSerializer, OrderSerializer
from .models import Product, CustomUser, Order


class ProductView(generics.ListCreateAPIView):
    """
    View all products or post a new one \n
    If account is provider, view all products \n
    If account is customer or anonymous, view only available for sale products \n
    If creating a new product, you can pass either one or many products in one request
    """
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly, IsProviderOrReadOnly)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if isinstance(kwargs['context']['request'].data, list):
            kwargs['many'] = True
        return serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)

    def get_queryset(self):
        if self.request.user.is_anonymous or not self.request.user.is_provider:
            return Product.available.all()
        return Product.objects.all()


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


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_provider:
            return Order.objects.filter(products__provider=self.request.user)
        return Order.objects.filter(user=self.request.user)


class LoginView(ObtainAuthToken):
    """
    Use this to obtain a token, pass this token to other requests with header:
    Authorization: Bearer 123456789abcdef
    """
    pass
