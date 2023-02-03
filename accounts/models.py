from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import datetime

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password=None,username=None):
        if not email:
            raise ValueError('Please Enter Email')
        if not password:
            raise ValueError('Please Enter Password')
        user=self.model(
            email  =  self.normalize_email(email),

        )
        user.is_active=True
        user.is_staff=False
        user.is_superuser=False
        user.is_verified=False
        user.set_password(password)
        user.save(using=self._db)
        return user
    


    def create_superuser(self,email,password):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
            
        )
       
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.is_verified=True
        user.set_password(password)
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100,unique=True)   
    mobile = models.CharField(max_length=10,unique=True,null=True)
    designation = models.CharField(max_length=50,null=False)
    password = models.CharField(max_length=220,blank=False,null=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD  ='email'
    REQUIRED_FIELDS=['password']
    objects = UserManager()

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

    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_superuser
    def has_module_perms(self,add_label):
        return True

############### Addition 01/02/23 #################################
    def create_branch_admin(self, email, password, branch_name):
        """
        Create and save a BranchAdmin user with the given email and password.
        """
        branch_admin = self.branchadmin_set.create(
            email=email,
            password=password,
            branch=Branch.objects.get(name=branch_name)
        )
        branch_admin.set_password(password)
        branch_admin.save()
        return branch_admin



class BranchAdmin(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    superadmin = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    # is_branchadmin = models.BooleanField(default=True)


class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    courses = models.ManyToManyField('Course')
    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Batch(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name



class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    time_needed = models.DurationField()
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=50)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)

class SubTopic(models.Model):
    name = models.CharField(max_length=50)
    topic = models.ManyToManyField(Topic)

############### AdditionEnds #################################