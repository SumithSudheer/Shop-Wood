# Generated by Django 4.0.7 on 2022-10-12 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_alter_cartitem_total_price_alter_cartitem_unit_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
