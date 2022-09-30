from django.contrib import admin
from django.urls import path
from order import views

urlpatterns = [
    path('/<t>/', views.homepage, name='index'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),

]