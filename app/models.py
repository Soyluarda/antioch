from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model




class ExtendedUser(AbstractUser):
    email = models.EmailField(null=False, unique=True)
    firma_bilgisi = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=100,null=True)
    telefon = models.CharField(max_length=100,null=True)
    firma_adi = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']