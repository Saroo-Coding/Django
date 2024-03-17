from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# tạo model từ db có sẵn: python manage.py inspectdb ra file models.py
# còn nếu chưa có db thì tạo bằng cơm xong đẩy lên database ngược lại vs dòng trên 
# Class khóa chính phải nằm trước class khóa phụ nếu class sau thì để 'nameClass'
# python manage.py makemigrations và python manage.py migrate để update model

class Category(models.Model):
    idcategory = models.BigAutoField(db_column='idCategory', primary_key=True)  # Field name made lowercase.
    created_at = models.DateTimeField()
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'

class Products(models.Model):
    idpro = models.BigAutoField(db_column='idPro', primary_key=True)  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    idcategory = models.ForeignKey(Category, models.DO_NOTHING, db_column='idCategory', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)
    unitprice = models.FloatField(db_column='unitPrice', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(blank=True, null=True)
    imgpro = models.TextField(db_column='imgPro', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'products'

class Payments(models.Model):
    idpay = models.BigAutoField(db_column='idPay', primary_key=True)  # Field name made lowercase.
    created_at = models.DateTimeField()
    paytype = models.IntegerField(db_column='payType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payments'

class Customer(models.Model):
    idcus = models.BigAutoField(db_column='idCus', primary_key=True)  # Field name made lowercase.
    created_at = models.DateTimeField()
    lastname = models.CharField(db_column='lastName', blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    pass_field = models.TextField(db_column='pass', blank=True, null=True)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'customer'


class Oder(models.Model):
    idoder = models.BigAutoField(db_column='idOder', primary_key=True)  # Field name made lowercase.
    oderdate = models.DateField(db_column='oderDate')  # Field name made lowercase.
    idcus = models.ForeignKey(Customer, models.DO_NOTHING, db_column='idCus', blank=True, null=True)  # Field name made lowercase.
    idpay = models.ForeignKey('Payments', models.DO_NOTHING, db_column='idPay', blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(blank=True, null=True)
    paydate = models.DateTimeField(db_column='payDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'oder'


class Cart(models.Model):
    iddetail = models.BigAutoField(db_column='idDetail', primary_key=True)  # Field name made lowercase.
    idpro = models.ForeignKey('Products', models.DO_NOTHING, db_column='idPro', blank=True, null=True)  # Field name made lowercase.
    quantity = models.BigIntegerField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    idcus = models.ForeignKey('Customer', models.DO_NOTHING, db_column='idCus', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cart'
