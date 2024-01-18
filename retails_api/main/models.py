from django.db import models
from django.contrib.auth.models import AbstractUser


class ProviderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_provider=True)


class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_provider=False)


class CustomUser(AbstractUser):
    is_provider = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    objects = models.Manager()
    providers = ProviderManager()
    customers = CustomerManager()

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    provider = models.ForeignKey(CustomUser,
                                 related_name='products',
                                 on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'provider']

    def __str__(self):
        return self.name
