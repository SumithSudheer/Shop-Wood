# Generated by Django 4.0.7 on 2022-09-23 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_cartitem_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(max_length=250)),
                ('coupon_code', models.CharField(max_length=50)),
                ('coupon_offer', models.IntegerField(max_length=3)),
                ('coupon_min', models.IntegerField(max_length=50)),
                ('coupon_start', models.DateTimeField(default=None)),
                ('coupon_end', models.DateTimeField(default=None)),
            ],
        ),
    ]
