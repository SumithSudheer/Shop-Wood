from datetime import datetime

from django.db import models
from  account.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True )
    offer = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category')
    image1 = models.ImageField(upload_to="project1/media/image/")
    image2 = models.ImageField(upload_to="project1/media/image/")
    image3 = models.ImageField(upload_to="project1/media/image/")
    image4 = models.ImageField(upload_to="project1/media/image/")

# class Cart(models.Model):
#     # cart_item = models.ForeignKey(CartItem, null=True, on_delete=models.CASCADE )
#     user = models.OneToOneField(User, null=True,   on_delete=models.CASCADE)
#     cart_id = models.BigAutoField(primary_key=True)

class CartItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='product')

    unit_price = models.DecimalField(max_digits=6, decimal_places=2,  null=True)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=6, decimal_places=2,  null = True)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

class Coupons(models.Model):
    coupon_name = models.CharField(max_length=250)
    coupon_code = models.CharField(max_length=50)
    coupon_offer = models.IntegerField(max_length=3)
    coupon_min = models.IntegerField(max_length=50)
    coupon_start = models.DateTimeField(default=None)
    coupon_end = models.DateTimeField(default=None)