# Generated by Django 4.0.7 on 2022-10-04 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_alter_payment_amount_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
