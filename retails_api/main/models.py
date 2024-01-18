from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_provider = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

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
