# Generated by Django 5.0.6 on 2024-09-19 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_vendoruser_contactpoint'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='manager',
            new_name='is_manager',
        ),
        migrations.RenameField(
            model_name='staff',
            old_name='sales',
            new_name='is_sales',
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Department Manager'),
        ),
    ]
