from django.db import models
from django.conf import settings
from uuid import uuid4
from os import path, remove

def uploadProjectFile(instance, filepath):
    ext = path.splitext(filepath)[1]
    return path.join('project', 'file', f'{uuid4()}{ext}')

def uploadProjectComment(instance, filepath):
    ext = path.splitext(filepath)[1]
    return path.join('project', 'comment', f'{uuid4()}{ext}')


class ProjectComment(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Project')
    file = models.FileField(upload_to=uploadProjectComment, blank=True, null=True, verbose_name='Comment File')
    comment = models.TextField(max_length=500, verbose_name='Comment')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Added By')
    added_on = models.DateTimeField(auto_now_add=True, verbose_name='Added On')
    objects = models.Manager()

    def __str__(self) -> str:
        return self.comment
    
    def delete(self):
        if self.file:
            self.file.delete()
        super().delete()

class ProjectFile(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Project')
    file = models.FileField(upload_to=uploadProjectFile, verbose_name='Project File')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Added By')
    added_on = models.DateTimeField(auto_now_add=True, verbose_name='Added On')
    objects = models.Manager()
    
    def delete(self):
        if self.file:
            self.file.delete()
        super().delete()

class Project(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Project Name')
    description = models.TextField(blank=True, verbose_name='Description')
    fabricator = models.ForeignKey('fabricator.Fabricator', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Fabricator')
    department = models.ForeignKey('department.Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Department')
    team = models.ForeignKey('team.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='projects', verbose_name='Teams')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='Project_Manager', verbose_name='Project Manager')
    status = models.CharField(max_length=55, default='ACTIVE', choices=[
        ('ACTIVE', 'Active'),
        ('ON-HOLD', 'On-Hold'),
        ('INACTIVE', 'Inactive'),
        ('DELAY', 'Delay'),
        ('COMPLETE', 'Complete'),
    ], blank=True, null=True, verbose_name='Project Status')
    stage = models.CharField(max_length=55, default='IFA', choices=[
        ('RFI', 'Request for Information'),
        ('IFA', 'Issue for Approval'),
        ('BFA', 'Back from Approval'),
        ('BFA-M', 'Back from Approval - Markup'),
        ('RIFA', 'Re-issue for Approval'),
        ('RBFA', 'Return Back from Approval'),
        ('IFC', 'Issue for Construction'),
        ('BFC', 'Back from Construction'),
        ('RIFC', 'Re-issue for Construction'),
        ('REV', 'Revision'),
        ('CO#', 'Change Order')
    ], blank=True, null=True, verbose_name='Project Stage')
    tool = models.CharField(max_length=20, default=None, choices=[
        ('TEKLA', 'TEKLA'),
        ('SDS-2', 'SDS-2')
    ], blank=True, null=True, verbose_name='Tools')
    connectionDesign = models.BooleanField(default=False, verbose_name="Connection Design")
    miscDesign = models.BooleanField(default=False, verbose_name="Misc Design")
    customerDesign = models.BooleanField(default=False, verbose_name="Customer Design")
    start_date = models.DateField(editable=True, verbose_name='Start Date')
    approval_date = models.DateField(editable=True, null=True, blank=True, verbose_name='Approval Date')
    is_bin = models.BooleanField(default=False, verbose_name='Recycle Bin')
    objects = models.Manager()

    def __str__(self):
        return self.name
    
    def add_file(self, file, user):
        file = ProjectFile.objects.create(
            project=self,
            file=file,
            added_by=user,
        )
        return file

    def get_all_file(self):
        return ProjectFile.objects.filter(project=self)
    
    def delete_file(self, file):
        file = ProjectFile.objects.get(pk=file)
        file.delete()
        return file
    
    def add_comment(self, comment, user, file=None):
        comment = ProjectComment.objects.create(
            project=self,
            file=file,
            comment=comment,
            added_by=user,
        )
        return comment
    
    def get_all_comment(self):
        return ProjectComment.objects.filter(project=self)
    
    def delete_comment(self, comment):
        comment = ProjectComment.objects.get(pk=comment)
        comment.delete()
        return comment