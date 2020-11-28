from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model




class ExtendedUser(AbstractUser):
    ad_soyad = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=False, unique=True)
    firma_adi = models.CharField(max_length=100,  null=True, blank=True)

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firma_adi']
    class Meta:
        verbose_name_plural = 'Kullanıcılar'