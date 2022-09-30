from django.db import models
from django.forms import fields
from .models import Product, Coupons
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ['title', 'price', 'category']

    def init(self, *args, **kwargs):
        super(ProductForm, self).init(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})

        self.fields['title'].widget.attrs.update({'class': 'form-control'})

        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})

        self.fields['inventory'].widget.attrs.update({'class': 'form-control'})

        self.fields['image1'].widget.attrs.update(
            {'class': 'form-control', 'id': 'id_image1', 'name': 'image', 'onchange': "changeImg(event)"})

        self.fields['image2'].widget.attrs.update(
            {'class': 'form-control', 'id': 'id_image1', 'name': 'image', 'onchange': "changeImg(event)"})

        self.fields['image3'].widget.attrs.update(
            {'class': 'form-control', 'id': 'id_image1', 'name': 'image', 'onchange': "changeImg(event)"})

        self.fields['image4'].widget.attrs.update(
            {'class': 'form-control', 'id': 'id_image1', 'name': 'image', 'onchange': "changeImg(event)"})


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupons
        fields = ['coupon_name', 'coupon_offer','coupon_code', 'coupon_min', 'coupon_start', 'coupon_end']