# Generated by Django 4.0.7 on 2022-10-11 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_alter_billing_address_order_id_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('1', 'COD'), ('2', 'RAZORPAY'), ('3', 'PAYPAL')], max_length=200),
        ),
    ]
