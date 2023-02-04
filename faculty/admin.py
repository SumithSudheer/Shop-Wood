from django.contrib import admin
from .models import faculty
from datetime import timedelta,datetime,date
 
# Register your models here.


class FacultyAdmin(admin.ModelAdmin):
        model=faculty
        list_display=('name','address','gender','district','contact_number_2','whatsapp_contact_number','date_of_birth','qualification','experiance_link','mode_of_class','email','password','is_staff','is_active','is_verified')
        readonly_fields=('last_login','joined_date','password')
        ordering=('joined_date',)
        



admin.site.register(faculty,FacultyAdmin)