from django.db import models
# from accounts.models import Account
# from adminside.models import Chapter,Course,topic
from datetime import timedelta,datetime,date
from rest_framework.validators import ValidationError
from rest_framework import serializers
# Create your models here.
class faculty(models.Model):
    name = models.CharField(max_length=255,null=True)
    address = models.TextField(null=True)
    # aadhar_number = models.CharField(max_length=12,null=True)
    photo=models.ImageField(null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    district = models.CharField(max_length=255,null=True)
    contact_number_2 = models.CharField(max_length=10,null=True)
    whatsapp_contact_number = models.CharField(max_length=10,null=True)
    date_of_birth = models.DateField(null=True)
    qualification = models.CharField(max_length=255,null=True)
    OFFLINE_ONLINE_CHOICES_exp = [
        ('1', 'Offline'),
        ('2', 'Online'),
    ]
    experiances = models.CharField(max_length=1, choices=OFFLINE_ONLINE_CHOICES_exp, blank=True, null=True)
    experiance_link = models.URLField(blank=True,null=True)
   
    # course = models.ManyToManyField(Course)
    # chapter = models.ManyToManyField(Chapter)
    # topic = models.ManyToManyField(topic)
    
    OFFLINE_ONLINE_CHOICES = [
        ('O', 'Offline'),
        ('L', 'Online'),
        ('B', 'Both'),
    ]
    mode_of_class  = models.CharField(max_length=1, choices=OFFLINE_ONLINE_CHOICES, blank=True,null=True)
    email=models.EmailField(unique=True,null=True)
    password=models.CharField(max_length=120,null=True)
    # pincode=models.IntegerField(null=True)
    # expected_salary=models.IntegerField(null=True)
    
    
    joined_date     =models.DateTimeField(auto_now_add=True,null=True)
    last_login      =models.DateTimeField(auto_now=True,null=True)
    is_staff        =models.BooleanField(default=False,null=True)
    is_active       =models.BooleanField(default=False,null=True)
    is_verified     =models.BooleanField(default=False,null=True)
    
    
    def get_date(self):
        time = datetime.now()
        if self.joined_date.day == time.day:
            return str(time.hour - self.joined_date.hour) + " hours ago"
        else:
            if self.joined_date.month == time.month:
                return str(time.day - self.joined_date.day) + " days ago"
            else:
                if self.joined_date.year == time.year:
                    return str(time.month - self.joined_date.month) + " months ago"
        return self.joined_date
   

