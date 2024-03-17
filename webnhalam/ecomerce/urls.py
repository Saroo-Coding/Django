from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Shop/', views.shop, name='shop'),
    path('Services/', views.services, name='services'),
    path('Contact/', views.contact, name='contact'),
    path('Cart/', views.cart, name='cart'),
    path('Login/', views.login_view, name='login'),
    path('Sign/', views.sign_view, name='sign'),
    path('Logout/', views.logout_view, name='logout'),
    
]