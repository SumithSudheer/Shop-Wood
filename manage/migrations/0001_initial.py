# Generated by Django 4.0.7 on 2022-09-10 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner1', models.ImageField(upload_to='project1/media/image/')),
                ('banner2', models.ImageField(upload_to='project1/media/image/')),
            ],
        ),
    ]
