from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class ProviderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_provider=True)


class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_provider=False)


class AvailableProductsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(open_for_sale=True)


class CustomUser(AbstractUser):
    is_provider = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    objects = UserManager()
    providers = ProviderManager()
    customers = CustomerManager()

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    open_for_sale = models.BooleanField(default=True)
    provider = models.ForeignKey(CustomUser,
                                 related_name='products',
                                 on_delete=models.CASCADE)

    objects = models.Manager()
    available = AvailableProductsManager()

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'provider']

    def __str__(self):
        return self.name
