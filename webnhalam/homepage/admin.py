from django.contrib import admin

from .models import Customer,Category,Payments,Products,Oderdetails,Oder

# Register your models here.
# CURD các model bằng admin

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Payments)
admin.site.register(Customer)
admin.site.register(Oder)
admin.site.register(Oderdetails)
