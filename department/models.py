from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Department Name')
    objects = models.Manager()

    def __str__(self):
        return self.name