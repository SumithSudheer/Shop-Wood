from django.db import models

# Create your models here.
class Banner(models.Model):
    banner1 = models.ImageField(upload_to='project1/media/image/')
    banner2 = models.ImageField(upload_to='project1/media/image/')