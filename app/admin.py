from django.contrib import admin
from django.contrib.auth.models import Group
from app.models import ExtendedUser
# Register your models here.

admin.site.register(ExtendedUser)

admin.site.unregister(Group)