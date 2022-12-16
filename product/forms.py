from django.db import models
from django.forms import fields
from .models import Product, Coupons
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def init(self, *args, **kwargs):
        super(ProductForm, self).init(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-group'})

        self.fields['title'].widget.attrs.update({'class': 'form-group'})

        self.fields['description'].widget.attrs.update({'class': 'form-group'})
        self.fields['price'].widget.attrs.update({'class': 'form-group'})

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
        fields = ['coupon_name', 'coupon_offer', 'coupon_code', 'coupon_min', 'coupon_start', 'coupon_end']

    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        self.fields['coupon_start'].label = "Coupon Start Date (YYYY-MM-DD)"

        self.fields['coupon_end'].label = "Coupon End Date (YYYY-MM-DD)"
