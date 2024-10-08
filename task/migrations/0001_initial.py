# Generated by Django 5.0.6 on 2024-08-16 11:04

import django.db.models.deletion
import task.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0005_project_description_alter_projectcomment_file'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Task Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('status', models.CharField(choices=[('ASSIGNED', 'Assigned'), ('IN-PROGRESS', 'In Progress'), ('ON-HOLD', 'On Hold'), ('BREAK', 'Break'), ('IN-REVIEW', 'In Review'), ('COMPLETE', 'Completed'), ('APPROVED', 'Approved')], default='ASSIGNED', max_length=255, verbose_name='Status')),
                ('priority', models.IntegerField(choices=[(0, 'Low'), (1, 'Normal'), (2, 'High'), (3, 'Critical')], default=1, verbose_name='Priority')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('duration', models.DurationField(verbose_name='Duration')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Created_By', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.task', verbose_name='Parent Task')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Task_Project', to='project.project', verbose_name='Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL, verbose_name='Current Assignee,')),
            ],
        ),
        migrations.CreateModel(
            name='AssignedList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved_on', models.DateTimeField(blank=True, null=True, verbose_name='Approved On')),
                ('assigned_on', models.DateTimeField(auto_now_add=True, verbose_name='Assigned On')),
                ('approved', models.BooleanField(default=False, verbose_name='Approval Status')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment on Approval')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to=settings.AUTH_USER_MODEL, verbose_name='Approved By')),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_by', to=settings.AUTH_USER_MODEL, verbose_name='Assigned By')),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to', to=settings.AUTH_USER_MODEL, verbose_name='Assigned To')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task', verbose_name='Task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=task.models.uploadTaskComment, verbose_name='Comment File')),
                ('comment', models.TextField(max_length=500, verbose_name='Comment')),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name='Added On')),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Added By')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task', verbose_name='Task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=task.models.uploadTaskFile, verbose_name='Task File')),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name='Added On')),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Added By')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task', verbose_name='Task')),
            ],
        ),
    ]
