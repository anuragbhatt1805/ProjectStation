from django.db import models
from django.conf import settings
from core.models import Staff

class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Department Name')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Department Manger', related_name='Department_Manager')
    is_bin = models.BooleanField(default=False, verbose_name='Recycle Bin')
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_staffs(self):
        return Staff.objects.filter(department=self)

    def add_staff(self, **user):
        try:
            user['department'] = self
            staff = Staff.objects.create(**user)
            return staff
        except Exception as E:
            print(E)
            raise E
        
    def remove_staff(self, pk=None):
        try:
            staff = Staff.object.get(pk=pk)
            staff.delete()
            return staff
        except Exception as E:
            print(E)
            raise E