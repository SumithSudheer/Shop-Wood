# Generated by Django 4.0.7 on 2022-10-04 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing_address',
            name='order_id_Ref',
            field=models.CharField(default=None, max_length=200),
        ),
    ]