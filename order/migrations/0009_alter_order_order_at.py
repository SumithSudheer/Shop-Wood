# Generated by Django 4.0.7 on 2022-09-18 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_order_order_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
