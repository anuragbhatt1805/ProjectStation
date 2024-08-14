# Generated by Django 5.0.6 on 2024-08-14 10:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_baseuser_username'),
        ('department', '0002_remove_department_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='User Address'),
        ),
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='User City'),
        ),
        migrations.AlterField(
            model_name='client',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='User Country'),
        ),
        migrations.AlterField(
            model_name='client',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='User State'),
        ),
        migrations.AlterField(
            model_name='client',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='User ZipCode'),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('designation', models.CharField(max_length=50, verbose_name='Staff Designation')),
                ('emp_code', models.CharField(max_length=15, unique=True, verbose_name='Employee Code')),
                ('manager', models.BooleanField(default=False, verbose_name='Department Manager')),
                ('sales', models.BooleanField(default=False, verbose_name='Sales Employee')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.department', verbose_name='Department')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.baseuser',),
        ),
    ]
