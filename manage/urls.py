from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import manage.views
from . import views

urlpatterns = [
    path('', views.index, name='admin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usermanagement/', views.usermanagement, name='usermanagement'),
    path('block_user/<id>/', views.block_user, name='block_user'),
    path('categorymanagement/', views.categorymanagement, name='categorymanagement'),
    path('editcategory/<id>/', views.editcategory, name='editcategory'),
    path('deletecategory/<id>/', views.deletecategory, name='deletecategory'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('productmanagement/', views.productmanagement, name='productmanagement'),
    path('deleteproduct/<id>/',views.deleteproduct, name='deleteproduct'),
    path('editproduct/<id>/',views.editproduct, name='editproduct'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('ordermanage/', views.order_manage, name='ordermanage'),
    path('ordercancel/<id>/', views.ordercancel, name='ordercancel'),
    path('order_status/<id>', views.delivery_status, name='delivery_status'),
    path('coupons/', views.coupon_management, name='coupons'),
    path('addcoupons/',views.add_coupons, name='addcoupons' ),
    path('addcoupons/',views.add_coupons, name='addcoupons' ),
    path('editcoupons/<id>/',views.edit_coupons, name='editcoupons'),
    path('salesreport/', views.sales_report, name='salesreport'),
]
