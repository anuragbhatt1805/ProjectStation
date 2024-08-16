from django.db import models
from django.conf import settings


class Member(models.Model):
    team = models.ForeignKey('team.Team', on_delete=models.CASCADE, verbose_name='Team')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Employee')
    role = models.CharField(max_length=50, default='GUEST', verbose_name='Role', choices=[
        ('GUEST', 'Guest'),
        ('LEADER', 'Leader'),
        ('MEMBER', 'Member'),
        ('MANAGER', 'Manager'),
        ('MODELER', 'Modeler'),
        ('CHECKER', 'Checker'),
        ('DETAILER', 'Detailer'),
        ('ERECTER', 'Erecter'),
        ('ADMIN', 'Admin')
    ])
    objects = models.Manager()

    def __str__(self):
        return self.employee.full_name()

class TeamManager(models.Manager):
    def create(self, **kwargs):
        team = self.model(**kwargs)
        team.save()
        leadMember = Member.objects.create(
            team = team,
            role = 'LEADER',
            employee = team.leader
        )
        leadMember.save()
        return team

class Team(models.Model):
    name = models.CharField(max_length=80, verbose_name='Team Name')
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Team Leader')
    department = models.ForeignKey('department.Department', on_delete=models.CASCADE, verbose_name='Team Department')
    is_bin = models.BooleanField(default=False, verbose_name='Recycle Bin')
    objects = TeamManager()

    def __str__(self):
        return self.name
    
    def get_members(self):
        return Member.objects.filter(team=self)
    
    def add_member(self, role, employee):
        member = Member.objects.create(
            team = self,
            role = role,
            employee = employee
        )
        member.save()
        return member
    
    def get_members_count(self):
        return self.get_members().count()
    
    def get_member_role(self, employee):
        return Member.objects.get(id=employee).role
    
    def remove_member(self, employee):
        member = Member.objects.get(id=employee)
        member.delete()
        return member