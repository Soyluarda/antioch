from django.db import models
from sorl.thumbnail import ImageField

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ürün Adı")
    description = models.TextField(verbose_name="Açıklama", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")
    image = ImageField(upload_to='products/', verbose_name="Ürün Resmi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Organik Ürün'
        verbose_name_plural = 'Organik Ürünler'
        ordering = ['-created_at']

