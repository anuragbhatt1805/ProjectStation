# Generated by Django 5.0.6 on 2024-08-16 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_project_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='is_active',
            new_name='is_bin',
        ),
    ]
