from django.db import models
from uuid import uuid4
from os import path
from django.conf import settings
from core.models import VendorUser


def uploadVendorDesign(instance, filepath):
    ext = path.splitext(filepath)[1]
    return path.join('vendorDesign', f'{uuid4()}{ext}')

class VendorDesign(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, verbose_name='Vendor')
    file = models.FileField(upload_to=uploadVendorDesign, verbose_name='vendor File')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Added By')
    added_on = models.DateTimeField(auto_now_add=True, verbose_name='Added On')
    objects = models.Manager()

    def delete(self):
        if self.file:
            self.file.delete()
        super().delete()

class Vendor(models.Model):
    name = models.CharField(max_length = 150, unique=True, verbose_name='Company Name')
    city = models.CharField(max_length=50, verbose_name='City')
    state = models.CharField(max_length=50, verbose_name='State')
    country = models.CharField(max_length=50, verbose_name='Country')
    zip_code = models.CharField(max_length=20, verbose_name='Zip Code')
    is_bin = models.BooleanField(default=False, verbose_name='Recycle Bin')
    objects = models.Manager()

    def __str__(self):
        return self.name
    
    def add_design(self, file, added_by):
        try:
            design = VendorDesign.objects.create(vendor=self, file=file, added_by=added_by)
            return design
        except:
            return False
    
    def list_design(self):
        return VendorDesign.objects.filter(vendor=self)
    
    def get_design(self, pk=None):
        try:
            return VendorDesign.objects.get(vendor=self, pk=pk)
        except:
            return False
        
    def remove_design(self, pk):
        try:
            design = VendorDesign.objects.get(vendor=self, pk=pk)
            design.delete()
            return True
        except:
            return False
        
    def list_all_user(self):
        return VendorUser.objects.filter(vendor=self)
    
    def add_user(self, **user):
        try:
            user['vendor'] = self
            vendor = VendorUser.objects.create_user(*user)
            return vendor
        except Exception as e:
            print(f"Error creating contact: {e}")
            raise e
    
    def  remove_user(self, pk=None):
        try:
            user = VendorUser.objects.get(vendor=self, pk=pk)
            user.delete()
            return user
        except:
            return False