from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import ExtendedUser
from django.contrib.auth import get_user_model


User = get_user_model()

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label="İsim")
    email = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label="E-mail Adresi")
    phone = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label="Telefon")
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control'}),label="İçerik")