from django.db import models

# Create your models here.


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
        ('Tesil', 'Tesil'),
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

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    detail = models.CharField(max_length=200)
    img = models.ImageField()
    desen = models.CharField(max_length=100,null=True,choices=DESEN,blank=True)
    renk = models.CharField(max_length=100,null=True,choices=RENK,blank=True)
    karisim = models.CharField(max_length=100,null=True,choices=KARISIM,blank=True)
    agirlik = models.CharField(max_length=100,null=True,choices=AGIRLIK,blank=True)
    siparis = models.CharField(max_length=100,null=True,choices=SIPARIS,blank=True)


    def __str__(self):
        return self.name

