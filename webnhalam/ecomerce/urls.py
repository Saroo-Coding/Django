from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='homeshop'),
    path('Shop/', views.shop, name='shop'),
    path('Services/', views.services, name='services'),
    path('Contact/', views.contact, name='contact'),

    #profile
    path('Profile/', views.profile, name='profile'),
    path('Coupon/', views.coupon, name='coupon'),

    #login & resigter
    path('Login/', views.login_view, name='login'),
    path('Sign/', views.sign_view, name='sign'),
    path('Logout/', views.logout_view, name='logout'),

    #cart
    path('Cart/', views.cart, name='cart'),
    path('addPro/', views.addPro, name='addPro'),
    path('updateCart/', views.updateCart, name='updateCart'),
    
    #bill
    path('Bill/', views.bill, name='bill'),
    path('Detail/<int:idDetail>', views.detail, name='detail'),
    path('pay/', views.pay, name='pay'),
    path('addCoupon/', views.addCoupon, name='addCoupon'),
]