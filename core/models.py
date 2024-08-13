from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, password=None, **kwargs):
        if not kwargs.get('username'):
            raise ValueError('The given username must be set')
        kwargs['email'] = self.normalize_email(kwargs.get('email', None))
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, **extra_fields):
        user = self.create_user(password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, primary_key=True, editable=False, verbose_name='Username')
    email = models.EmailField(max_length=150, null=True, blank=True, verbose_name='Email')
    f_name = models.CharField(max_length=50, verbose_name='First Name')
    m_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Middle Name')
    l_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Last Name')
    phone = models.CharField(max_length=15, verbose_name='Phone Number')
    role = models.CharField(max_length=10, choices=[
        ('STAFF', 'Staff'),
        ('CLIENT', 'Client'),
        ('VENDOR', 'Vendor'),
    ], verbose_name='Role for User')
    is_active = models.BooleanField(default=True, verbose_name='Active User')
    is_staff = models.BooleanField(default=False, verbose_name='WBT Employee')
    is_superuser = models.BooleanField(default=False, verbose_name='Administrator')

    object = UserManager()

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