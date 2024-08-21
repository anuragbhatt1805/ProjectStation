from django.db import models
from django.conf import settings
from uuid import uuid4
from os import path, remove
from datetime import datetime

def uploadTaskFile(instance, filepath):
    ext = path.splitext(filepath)[1]
    return path.join('task', 'file', f'{uuid4()}{ext}')

def uploadTaskComment(instance, filepath):
    ext = path.splitext(filepath)[1]
    return path.join('task', 'comment', f'{uuid4()}{ext}')

class TaskComment(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Task')
    file = models.FileField(upload_to=uploadTaskComment, null=True, blank=True, verbose_name='Comment File')
    comment = models.TextField(max_length=500, verbose_name='Comment')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Added By')
    added_on = models.DateTimeField(auto_now_add=True, verbose_name='Added On')
    tags = models.ManyToManyField('tag.Tag', blank=True, verbose_name='Tags')
    objects = models.Manager()

    def __str__(self) -> str:
        return self.comment
    
    def delete(self):
        if self.file:
            self.file.delete()
        super().delete()

class TaskFile(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Task')
    file = models.FileField(upload_to=uploadTaskFile, verbose_name='Task File')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Added By')
    added_on = models.DateTimeField(auto_now_add=True, verbose_name='Added On')
    objects = models.Manager()
    
    def delete(self):
        if self.file:
            self.file.delete()
        super().delete()

class AssignedList(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Task')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_by', verbose_name='Assigned By')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_to', verbose_name='Assigned To')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approved_by', verbose_name='Approved By', blank=True, null=True)
    approved_on = models.DateTimeField(verbose_name='Approved On', null=True, blank=True)
    assigned_on = models.DateTimeField(auto_now_add=True, verbose_name='Assigned On')
    approved = models.BooleanField(default=False, verbose_name='Approval Status')
    comment = models.TextField(blank=True, verbose_name='Comment on Approval', null=True)
    objects = models.Manager()

    def confirm(self, approved_by, comment=None):
        self.approved_by = approved_by
        self.approved_on = datetime.now()
        if comment:
            self.comment = comment
        self.approved = True
        self.save()
        self.task.user = self.assigned_to
        self.task.status = "ASSINGED"
        self.task.save()
        return self

class TaskPriority(models.IntegerChoices):
    LOW = 0, 'Low'
    NORMAL = 1, 'Normal'
    HIGH = 2, 'High'
    CRITICAL = 3, 'Critical'

class TaskManager(models.Manager):
    def create(self, assigned_by, **kwargs):
        task = self.model(**kwargs)
        task.save()
        task.add_assignes(
            assigned_by=assigned_by,
            assigned_to=kwargs.get('user'),
            approved_by=assigned_by,
            approved_on=datetime.now(),
            approved=True,
            comment=None
        )
        
        return task  # Return the created task object

class Task(models.Model):
    name = models.CharField(max_length=150, verbose_name='Task Name')
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, verbose_name='Project', related_name='Task_Project')
    parent = models.ForeignKey('Task', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Parent Task')
    description = models.TextField(blank=True, verbose_name='Description')
    status = models.CharField(max_length=255, blank=False, verbose_name='Status', choices=[
        ('ASSIGNED', 'Assigned'),
        ('IN-PROGRESS', 'In Progress'),
        ('ON-HOLD', 'On Hold'),
        ('BREAK', 'Break'),
        ('IN-REVIEW', 'In Review'),
        ('COMPLETE', 'Completed'),
        ('APPROVED', 'Approved')
    ], default='ASSIGNED')
    priority = models.IntegerField(blank=False, verbose_name='Priority', choices=TaskPriority.choices, default=TaskPriority.NORMAL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Current Assignee,', related_name='User')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Created By', related_name='Created_By')
    created_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(verbose_name='Due Date')
    duration = models.DurationField(verbose_name='Duration')
    is_bin = models.BooleanField(default=False, verbose_name='Recycle Bin')
    objects = TaskManager()

    def __str__(self) -> str:
        return self.name
    
    def get_child_tasks(self):
        return Task.objects.filter(parent=self)
    
    def get_assignes(self):
        return AssignedList.objects.filter(task=self)
    
    def add_assignes(self, **extra_kwargs):
        assignList = AssignedList.objects.create(
            task=self,
            assigned_by=extra_kwargs.get('assigned_by'),
            assigned_to=extra_kwargs.get('assigned_to'),
            approved_by=extra_kwargs.get('approved_by', None),
            approved_on=extra_kwargs.get('approved_on', None),
            approved=extra_kwargs.get('approved', False),
            comment=extra_kwargs.get('comment', None),
        )
        assignList.save()
        return assignList
    
    def update_assignes(self, id, **extra_kwargs):
        assignList = AssignedList.objects.get(id)
        assignList.assigned_by = extra_kwargs.get('assigned_by', assignList.assigned_by)
        assignList.assigned_to = extra_kwargs.get('assigned_to', assignList.assigned_to)
        assignList.approved_by = extra_kwargs.get('approved_by', assignList.approved_by)
        assignList.approved_on = datetime.now()
        assignList.approved = True
        assignList.comment = extra_kwargs.get('comment', assignList.comment)
        assignList.save()
        self.user = assignList.assigned_to
        self.save()
        return assignList
    
    def get_all_file(self):
        return TaskFile.objects.filter(task=self)
    
    def add_file(self, file, user):
        taskFile = TaskFile.objects.create(
            task=self,
            file=file,
            added_by=user,
        )
        return taskFile

    def delete_file(self, file):
        file = TaskFile.objects.get(pk=file)
        file.delete()
        return file

    def get_all_comment(self):
        return TaskComment.objects.filter(task=self)
    
    def add_comment(self, comment, user, file=None):
        taskComment = TaskComment.objects.create(
            task=self,
            file=file,
            comment=comment,
            added_by=user,
        )
        return taskComment
    
    def delete_comment(self, comment):
        comment = TaskComment.objects.get(pk=comment)
        comment.delete()
        return comment