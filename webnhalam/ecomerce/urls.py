from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Shop/', views.shop, name='shop'),
    path('Services/', views.services, name='services'),
    path('Contact/', views.contact, name='contact'),
    path('Cart/', views.cart, name='cart'),
    
]