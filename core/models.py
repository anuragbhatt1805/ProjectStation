from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# USER MANAGER CLASS
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        email = self.normalize_email(None if extra_fields.get('email') in [None, '', ['']] else extra_fields.get('email', None))
        extra_fields['email'] = email
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(username, password, **extra_fields)


# BASE USER CLASS
class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, verbose_name='Username')
    email = models.EmailField(max_length=150, null=True, blank=True, verbose_name='Email')
    f_name = models.CharField(max_length=50, verbose_name='First Name')
    m_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Middle Name')
    l_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Last Name')
    phone = models.CharField(max_length=20, verbose_name='Phone Number')
    role = models.CharField(max_length=10, choices=[
        ('STAFF', 'Staff'),
        ('CLIENT', 'Client'),
        ('VENDOR', 'Vendor'),
    ], verbose_name='Role for User')
    is_active = models.BooleanField(default=True, verbose_name='Active User')
    is_staff = models.BooleanField(default=False, verbose_name='Department Manager')
    is_superuser = models.BooleanField(default=False, verbose_name='Administrator')
    is_firstLogin = models.BooleanField(default=True, verbose_name='Change Password on Next Login')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['f_name', 'phone', 'role']
    
    def __str__(self):
        return self.username
    
    def full_name(self):
        if self.l_name and self.m_name:
            return f"{self.f_name} {self.m_name} {self.l_name}"
        elif self.l_name:
            return f"{self.f_name} {self.l_name}"
        return self.f_name


# CLIENT MANAGER CLASS
class ClientManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'CLIENT')
        return super().create_user(username, password, **extra_fields)

# CLIENT CLASS
class Client(BaseUser):
    fabricator = models.ForeignKey('fabricator.Fabricator', on_delete=models.CASCADE, verbose_name='Client Company/Fabricator')
    alt_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Alternate Phone')
    designation = models.CharField(max_length=50, verbose_name='Client Designation')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='User Address')
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name='User City')
    state = models.CharField(max_length=50, null=True, blank=True, verbose_name='User State')
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name='User Country')
    zip_code = models.CharField(max_length=10, null=True, blank=True, verbose_name='User ZipCode')

    objects = ClientManager()

    def __str__(self):
        return f"{self.full_name()} ({self.username})"


# STAFF MANAGER CLASS
class StaffManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'STAFF')
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser'):
            extra_fields.setdefault('is_manager', True)
            extra_fields.setdefault('is_sales', True)
        return super().create_user(username, password, **extra_fields)

class Staff(BaseUser):
    department = models.ForeignKey('department.Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Department", related_name='Staff_Department')
    designation = models.CharField(max_length=50, verbose_name='Staff Designation')
    emp_code = models.CharField(max_length=15, unique=True, verbose_name='Employee Code')
    is_manager = models.BooleanField(default=False, verbose_name='Project Manager')
    is_sales = models.BooleanField(default=False, verbose_name='Sales Employee')

    objects = StaffManager()

    def __str__(self):
        return f"{self.full_name()} ({self.username})"

class VendorUserManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'VENDOR')
        return super().create_user(username, password, **extra_fields)

class VendorUser(BaseUser):
    vendor = models.ForeignKey('vendor.Vendor', on_delete=models.CASCADE, verbose_name='Vendor Company')
    title = models.CharField(max_length=30, verbose_name='User Designation')
    contactPoint = models.BooleanField(default=False, verbose_name='Point of contact')
    objects = VendorUserManager()

    def __str__(self):
        return f"{self.full_name()} ({self.username})"