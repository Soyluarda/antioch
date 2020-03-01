from django.db import models
import jsonfield

# Create your models here.

from product.models import Product, Upholstery

class Cart(models.Model):
    products = models.ManyToManyField(Product,null=True,blank=True)
    upholsteries = models.ManyToManyField(Upholstery,null=True,blank=True)
    details = jsonfield.JSONField()
    total = models.DecimalField(max_digits=100,decimal_places=2,default=0.00)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return "Cart id: %s" %(self.id )