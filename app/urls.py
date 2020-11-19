from django.urls import path,re_path
from .views import *
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(6000 * 1000)(index),name='index'),
    path('giris/', auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('kayit-ol/', signup, name='signup'),
    path('urunler', cache_page(6000 * 1000)(products),name='products'),
    path('sepet', carts,name='carts'),
    re_path('sepet/(?P<slug>[\w-]+)/$', update_carts,name='update_carts'),
    re_path('sepet2/(?P<slug>[\w-]+)/$', update_carts_2,name='update_carts_2'),
    re_path('sepet4/(?P<slug>[\w-]+)/$', update_carts_up, name='update_carts_up'),
    re_path('sepet5/(?P<slug>[\w-]+)/$', update_carts_up_2, name='update_carts_up_2'),
    re_path('sepet3/$', update_carts_3, name='update_carts_3'),
    path('upholstery', cache_page(6000 * 1000)(upholstery),name='upholstery'),
    path('agents', agents, name='agents'),
    path('fairs', fairs, name='fairs'),
    path('stok', stock_service,name='stock_service'),
    path('iletisim', contact, name='contact'),
    path('hakkimizda', about, name='about'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    path('passwordchange', change_password, name='change_password'),
    path('sifremi-unuttum/', auth_views.PasswordResetView.as_view(template_name='admin/registration/password_reset_form.html'), name='password_reset'),
    path('^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='admin/registration/password_reset_done.html'), name='password_reset_done'),
    re_path('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='admin/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='admin/registration/password_reset_complete.html'), name='password_reset_complete'),
]
