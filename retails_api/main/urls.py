from django.urls import path

from . import views

urlpatterns = [
    path('ping/', views.HelloWorldView.as_view(), name='hello_world'),
]
