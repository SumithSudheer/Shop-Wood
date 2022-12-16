from django.utils import timezone

from django.db import models
from account.models import User

# Create your models here.



import product.models


class Order(models.Model):
    payment_choice1 = (
        ("1", "COD"),
        ("2", "RAZORPAY"),
        ("3", "PAYPAL"),

    )
    delivery_status_choice =(
        ("P","Pending"),
        ("S","Shipped"),
        ("D","Deliverd")
    )



    user = models.ForeignKey(User, on_delete=models.PROTECT )
    product = models.ForeignKey(product.models.Product, on_delete=models.PROTECT)
    # product_name = models.CharField(max_length=250, null=False)
    purchase_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    total_price= models.DecimalField(max_digits=6, decimal_places=2)
    payment_id = models.CharField(max_length=200, null=True )
    payment_method = models.CharField(max_length=200, choices=payment_choice1)
    payment_status = models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=200, choices=delivery_status_choice, default="P")
    status = models.BooleanField(default=True)
    order_at = models.DateTimeField(auto_now_add=True )
    order_id = models.CharField(max_length=200, default=None)



class Billing_address(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=225)
    address1 = models.TextField(max_length=250)
    address2 = models.TextField(max_length=250)
    country = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    zip = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=False)
    order = models.OneToOneField(Order, on_delete=models.PROTECT)
    order_id_Ref = models.CharField(max_length=200, default=None)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=120)
    payment_method = models.CharField(max_length=120)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=200, default=None, unique=True)