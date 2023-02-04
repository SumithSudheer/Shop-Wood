
from rest_framework import serializers
from . import models
from datetime import timedelta
# from adminside.models import Chapter
from django.core.validators import RegexValidator
from rest_framework.validators import ValidationError
import json
from django.contrib.auth.hashers import make_password


class FacultySerializer(serializers.ModelSerializer):
    # course = serializers.ListField(required=True)
    email = serializers.EmailField(required=True)
    whatsapp_contact_number = serializers.CharField(min_length=10,required=True)
    # pincode = serializers.CharField(validators=[RegexValidator('^[0-9]{6}$', 'Enter a valid 6-digit PIN code.')])
    qualification = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    district = serializers.CharField(required=True,min_length=4)
    class Meta:
        model = models.faculty
        fields = ('name', 'address', 'gender', 'district', 'contact_number_2', 'whatsapp_contact_number', 'date_of_birth', 'qualification', 'experiances', 'experiance_link','mode_of_class','email','password')








