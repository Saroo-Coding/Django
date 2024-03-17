from django.contrib import admin

from .models import Customer,Category,Payments,Products,Cart,Oder

# Register your models here.
# py manage.py createsuperuser tạo tk admin
# CURD các model bằng admin

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Payments)
admin.site.register(Customer)
admin.site.register(Oder)
admin.site.register(Cart)