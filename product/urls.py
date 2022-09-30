# from django.urls import path
from . import views
# from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from imageapp import views

urlpatterns = [
    path('', views.product_home, name='product_home'),
    path('productview/<id>/', views.productview, name='productview'),
    path('products/', views.products, name='products'),
    path('products/<id>/', views.productsf, name='productsf'),
    path('addtocart/<id>/', views.addtocart, name='addtocart'),
    path('viewcart/', views.viewCart, name='viewcart'),
    path('checkout/', views.check_out, name='checkout'),
    path('order/', views.user_order, name='order'),
    path('order/<id>/', views.order_cancel, name='order'),
    path('iquantity/<id>/', views.iquantity_cart, name='iquantity'),
    path('dquantity/<id>/', views.dquantity_cart, name='dquantity'),
    path('removecart/<id>/', views.remove_cart, name='removecart'),
    path('razor/', views.razor_home, name='razor'),
    path('success/', views.success, name='success'),
    path('successp/', views.successp, name='successp'),
    path('payments/', views.payments, name='payments'),
    path('test/', views.test, name='test'),
    path('order_view/<id>/', views.order_view, name='order_view'),
    path('couponapply/', views.coupon_apply, name='couponapply'),
    path('couponremove/', views.coupon_remove, name='couponremove')

]
