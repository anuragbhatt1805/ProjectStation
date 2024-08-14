# Generated by Django 5.0.6 on 2024-08-14 07:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('fabricator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='fabricator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fabricator.fabricator', verbose_name='Client Company/Fabricator'),
        ),
    ]
