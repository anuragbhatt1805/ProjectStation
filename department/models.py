from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Department Name')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Department Manger', related_name='Department_Manager')
    is_bin = models.BooleanField(default=False, verbose_name='Recycle Bin')
    objects = models.Manager()

    def __str__(self):
        return self.name