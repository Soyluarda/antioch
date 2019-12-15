from django.urls import path,re_path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index,name='index'),
    path('index2/', index2,name='index2'),
    path('Anasayfa2/', index3,name='index3'),
    path('signup/', signup, name='signup'),
    path('ürünler', products,name='products'),
    path('iletisim', contact, name='contact'),
    path('hakkimizda', about, name='about'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    path('passwordchange', change_password, name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

]
