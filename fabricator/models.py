from django.db import models
from uuid import uuid4
from os import path, remove
from django.conf import settings
from core.models import Client


def uploadStandardDesign(instance, filepath):
    ext = path.splitext(filepath)[1]
    return path.join('standardDesign', f'{uuid4()}{ext}')

class StandardDesign(models.Model):
    fabricator = models.ForeignKey('Fabricator', on_delete=models.CASCADE, verbose_name='Fabricator')
    file = models.FileField(upload_to=uploadStandardDesign, verbose_name='Design File')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Added By')
    added_on = models.DateTimeField(auto_now_add=True, verbose_name='Added On')
    objects = models.Manager()

    def delete(self):
        if self.file:
            self.file.delete()
        super().delete()

class Fabricator(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Fabricator Name")
    # department = models.ForeignKey('department.Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Department")
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name='Billing Address')
    city = models.CharField(max_length=50, verbose_name='City')
    state = models.CharField(max_length=50, verbose_name='State')
    country = models.CharField(max_length=50, verbose_name='Country')
    zip_code = models.CharField(max_length=20, verbose_name='Zip Code')
    website = models.CharField(max_length=50, null=True, blank=True, verbose_name='Fabricator Website')
    drive = models.CharField(max_length=255, null=True, blank=True, verbose_name='Drive URL')
    is_bin = models.BooleanField(default=False, verbose_name='Recycle Bin')
    objects = models.Manager()

    def __str__(self):
        return self.name
    
    def list_design(self):
        return StandardDesign.objects.filter(fabricator=self)
    
    def get_design(self, pk=None):
        try:
            return StandardDesign.objects.get(fabricator=self, pk=pk)
        except:
            return False
    
    def add_design(self, file, added_by):
        try:
            design = StandardDesign.objects.create(fabricator=self, file=file, added_by=added_by)
            return design
        except:
            return False
    
    def remove_design(self, pk):
        try:
            design = StandardDesign.objects.get(fabricator=self, pk=pk)
            design.delete()
            return True
        except:
            return False
    
    def list_contact(self):
        return Client.objects.filter(fabricator=self)
    
    def get_contact(self, pk=None):
        try:
            return Client.objects.get(fabricator=self, pk=pk)
        except:
            return False

    def add_contact(self, **user):
        try:
            user['fabricator'] = self
            user['address'] = user.get('address', self.address)
            user['city'] = user.get('city') if user.get('city') not in [None, '', ['']] else self.city
            user['state'] = user.get('state') if user.get('state') not in [None, '', ['']] else self.state
            user['country'] = user.get('country') if user.get('country') not in [None, '', ['']] else self.country
            user['zip_code'] = user.get('zip_code') if user.get('zip_code') not in [None, '', ['']] else self.zip_code
            contact = Client.objects.create_user(**user)
            return contact
        except Exception as e:
            print(f"Error creating contact: {e}")
            raise e  
    def remove_contact(self, pk=None):
        try:
            contact = Client.objects.get(fabricator=self, pk=pk)
            contact.delete()
            return contact
        except:
            return False