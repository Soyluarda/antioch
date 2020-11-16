from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import ExtendedUser
from django.contrib.auth import get_user_model


User = get_user_model()

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = ExtendedUser
        fields = ('username','email','firma_bilgisi','address','telefon','firma_adi','password1', 'password2')



class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label="İsim")
    email = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label="E-mail Adresi")
    phone = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label="Telefon")
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control'}),label="İçerik")