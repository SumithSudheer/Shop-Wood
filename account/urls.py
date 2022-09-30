from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('signin/', views.index, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('otplogin/', views.otp, name='otplogin'),
    path('otp/', views.otp_verify, name='otp'),
    path('logout/', views.logout_user, name='logout'),
    path('user/', views.account_view, name='user'),
    path('changepass/', views.change_pass, name='changepass'),
    path('address/', views.address_manage, name='address'),
    path('editaddress/<id>/', views.edit_address, name='editaddress'),

]