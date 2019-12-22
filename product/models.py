from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    detail = models.CharField(max_length=200)
    img = models.ImageField()

    def __str__(self):
        return self.name

