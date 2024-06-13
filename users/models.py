from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_seller = True
        user.is_customer = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_admin = True
        user.is_seller = True
        user.is_customer = True
        user.save(using=self._db)
        return user
    
    def create_seller(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_active = False
        user.is_seller = True
        user.save(using=self._db)
        return user
    
    def create_customer(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_active = True
        user.is_customer = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    # Additional fields
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_permissions', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff_user(self):
        "Is the user a member of staff?"
        return self.is_staff

    @property
    def is_admin_user(self):
        "Is the user an admin member?"
        return self.is_admin

    @property
    def is_customer_user(self):
        "Is the user an admin member?"
        return self.is_customer
    
    @property
    def is_seller_user(self):
        "Is the user an admin member?"
        return self.is_seller


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30,null=True,blank=True) 
    last_name = models.CharField(max_length=30,null=True,blank=True)
    phone = models.BigIntegerField(null=True,blank=True)
    updated_on =  models.DateTimeField('updated on', default=timezone.now)
    address = models.CharField(max_length=800,blank=True,null=True)
    country = models.CharField(max_length=200,blank=True,null=True)
    state = models.CharField(max_length=30,blank=True,null=True)
    city = models.CharField(max_length=30,null=True,blank=True)
    pin_code = models.CharField(max_length=6,null=True,blank=True)
    
    
    
class OTP(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,null=False)
    email = models.EmailField(unique=True, null=True)
    otp = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    