from . import views
from django.urls import path
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
    path('iquantity/', views.iquantity_cart, name='iquantity'),
    path('dquantity/', views.dquantity_cart, name='dquantity'),
    path('removecart/<id>/', views.remove_cart, name='removecart'),
    path('success/', views.success, name='success'),
    path('successp/', views.successp, name='successp'),
    path('payments/', views.payments, name='payments'),
    path('order_view/<id>/', views.order_view, name='order_view'),
    path('couponremove/', views.coupon_remove, name='couponremove')

]
