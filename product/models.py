from django.db import models
from sorl.thumbnail import ImageField
import os
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
import asyncio
import time
import random


async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()

        # Sleep for the "sleep_for" seconds.
        await asyncio.sleep(sleep_for)
        os.system('python3 manage.py collectstatic --noinput')
        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()

    # Generate random timings and put them into the queue.
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(1, 5)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')



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
        asyncio.run(main())

    class Meta:
        verbose_name_plural = 'ürünler'

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
        asyncio.run(main())



