from django.db import models
from sorl.thumbnail import ImageField
import os
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import sync_to_async
import asyncio
import time
import random
import django_rq


def update_products(delay):
    time.sleep(delay)
    os.system('python3 manage.py collectstatic --noinput')

class Product(models.Model):
    DESEN = [
        ('ekose', 'ekose'),
        ('Etnik', 'Etnik'),
        ('Geometrik', 'Geometrik'),
        ('Baliksirti', 'Baliksirti'),
        ('Kazayagi', 'Kazayagi'),
        ('Duz', 'Duz'),
        ('Cizgi', 'Cizgi'),
        ('Tweed', 'Tweed'),
    ]
    RENK = [
        ('Bej', 'Bej'),
        ('Siyah', 'Siyah'),
        ('Beyaz', 'Beyaz'),
        ('Mavi', 'Mavi'),
        ('Lacivert', 'Lacivert'),
        ('Kahverengi', 'Kahverengi'),
        ('Camel', 'Camel'),
        ('Yesil', 'Yesil'),
        ('Haki', 'Haki'),
        ('Turuncu', 'Turuncu'),
        ('Pembe', 'Pembe'),
        ('Kirmizi', 'Kirmizi'),
        ('Bordo', 'Bordo'),
        ('Mor', 'Mor'),
        ('Sari', 'Sari'),
        ('Gri', 'Gri'),
        ('Antrasit', 'Antrasit'),
        ('Multicolor', 'Multicolor'),
    ]
    KARISIM = [
        ('Akrilik', 'Akrilik'),
        ('Alpaka', 'Alpaka'),
        ('Angora', 'Angora'),
        ('Kasmir', 'Kasmir'),
        ('Pamuk', 'Pamuk'),
        ('Elastan', 'Elastan'),
        ('Keten', 'Keten'),
        ('Polyamid', 'Polyamid'),
        ('Polyester', 'Polyester'),
        ('Ipek', 'Ipek'),
        ('Moher', 'Moher'),
        ('Yun', 'Yun'),
        ('Viskon', 'Viskon'),

    ]

    AGIRLIK = [
        ('0-200 g/mtul', '0-200 g/mtul'),
        ('201-400g/mtul', '201-400g/mtul'),
        ('401-600g/mtul', '401-600g/mtul'),
        ('600+ g/mtul', '600+ g/mtul'),
    ]
    SIPARIS = [
        ('1-100', '1-100 '),
        ('101-300', '101-300'),
        ('301-500', '301-500'),
        ('500+', '500+'),
    ]

    name = models.CharField(max_length=100, verbose_name="başlık")
    name_en = models.CharField(max_length=100, verbose_name="ingilizce başlık", blank=True)
    name_ru = models.CharField(max_length=100, verbose_name="rusça başlık", blank=True)
    price = models.IntegerField(verbose_name="fiyat")
    detail = models.CharField(max_length=200, verbose_name="detay")
    img = ImageField(upload_to='urunler', verbose_name="resim")
    desen = models.CharField(max_length=100,null=True,choices=DESEN,blank=True)
    renk = models.CharField(max_length=100,null=True,choices=RENK,blank=True)
    karisim = models.CharField(max_length=100,null=True,choices=KARISIM,blank=True)
    agirlik = models.CharField(max_length=100,null=True,choices=AGIRLIK,blank=True)
    siparis = models.CharField(max_length=100,null=True,choices=SIPARIS,blank=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        queue = django_rq.get_queue('default')
        queue.enqueue('product.models.update_products', 5)

    class Meta:
        verbose_name_plural = 'ürünler'


def update_upholsteries(delay):
    time.sleep(delay)
    os.system('python3 manage.py collectstatic --noinput')

class Upholstery(models.Model):
    RENK = [
        ('Bej', 'Bej'),
        ('Siyah', 'Siyah'),
        ('Beyaz', 'Beyaz'),
        ('Mavi', 'Mavi'),
        ('Lacivert', 'Lacivert'),
        ('Kahverengi', 'Kahverengi'),
        ('Camel', 'Camel'),
        ('Yesil', 'Yesil'),
        ('Haki', 'Haki'),
        ('Turuncu', 'Turuncu'),
        ('Pembe', 'Pembe'),
        ('Kirmizi', 'Kirmizi'),
        ('Bordo', 'Bordo'),
        ('Mor', 'Mor'),
        ('Sari', 'Sari'),
        ('Gri', 'Gri'),
        ('Antrasit', 'Antrasit'),
        ('Multicolor', 'Multicolor'),
    ]
    name = models.CharField(max_length=100, verbose_name="başlık")
    name_en = models.CharField(max_length=100, verbose_name="ingilizce başlık", blank=True)
    name_ru = models.CharField(max_length=100, verbose_name="rusça başlık", blank=True)
    img = ImageField(upload_to="dosemelik", verbose_name="resim")
    renk = models.CharField(max_length=100, null=True, choices=RENK, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Döşemelikler'


    def save(self, *args, **kwargs):
        super(Upholstery, self).save(*args, **kwargs)
        queue = django_rq.get_queue('default')
        queue.enqueue('product.models.update_upholsteries', 5)

