# Generated by Django 5.0.6 on 2024-08-14 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabricator',
            name='drive',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Drive URL'),
        ),
        migrations.AddField(
            model_name='fabricator',
            name='website',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Fabricator Website'),
        ),
    ]
