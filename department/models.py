from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Department Name')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Department Manager')
    is_sales = models.BooleanField(default=False, verbose_name='Is Sales')
    objects = models.Manager()

    def __str__(self):
        return self.name