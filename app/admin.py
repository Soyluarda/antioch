from django.contrib import admin
from app.models import ExtendedUser
# Register your models here.
from cart.models import Cart

admin.site.register(ExtendedUser)

class CartAdmin(admin.ModelAdmin):
    class Meta:
        model = Cart


admin.site.register(Cart,CartAdmin)