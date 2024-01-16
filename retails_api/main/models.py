from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    provider = models.ForeignKey(User,
                                 related_name='products',
                                 on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'provider']

    def __str__(self):
        return self.name
