from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductView.as_view(), name='products-list'),
    path('users/', views.UserList.as_view(), name='users-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='users-detail'),
]
