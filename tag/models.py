from django.db import models


class Tag(models.Model):
    name = models.CharField(unique=True, verbose_name='HashTag')
    objects = models.Manager()

    def __str__(self):
        return self.name