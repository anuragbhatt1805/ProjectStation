from django.db import models
from uuid import uuid4
from os import path
from django.conf import settings


def uploadStandardDesign(instance, filepath):
    ext = path.splittext(filepath)[1]
    return path.join('standardDesign', f'{uuid4()}{ext}')

class StandardDesign(models.Model):
    fabricator = models.ForeignKey('Fabricator', on_delete=models.CASCADE, verbose_name='Fabricator')
    file = models.FileField(upload_to=uploadStandardDesign, verbose_name='Design File')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Added By')
    added_on = models.DateTimeField(auto_now_add=True, verbose_name='Added On')
    objects = models.Manager()

class Fabricator(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Fabricator Name")
    department = models.ForeignKey('department.Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Department")
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name='Billing Address')
    city = models.CharField(max_length=50, verbose_name='City')
    state = models.CharField(max_length=50, verbose_name='State')
    country = models.CharField(max_length=50, verbose_name='Country')
    zip_code = models.CharField(max_length=20, verbose_name='Zip Code')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    objects = models.Manager()

    def __str__(self):
        return self.name
    
    def list_design(self):
        return StandardDesign.objects.filter(fabricator=self)
    
    def count_all_design(self):
        return StandardDesign.objects.filter(fabricator=self).count()
    
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
    
    def delete_design(self, pk):
        try:
            design = StandardDesign.objects.get(fabricator=self, pk=pk)
            design.delete()
            return True
        except:
            return False