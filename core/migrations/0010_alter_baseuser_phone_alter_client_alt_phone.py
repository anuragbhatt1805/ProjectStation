# Generated by Django 5.0.6 on 2024-09-20 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_baseuser_is_firstlogin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='client',
            name='alt_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Alternate Phone'),
        ),
    ]
