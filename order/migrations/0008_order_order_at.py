# Generated by Django 4.0.7 on 2022-09-18 06:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
