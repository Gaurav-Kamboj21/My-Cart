from django.contrib import admin
from .models import Products, Contact, Orders, OrderUpdate, Users
# Register your models here.
admin.site.register(Products)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(Users)
