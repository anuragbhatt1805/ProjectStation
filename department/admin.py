from django.contrib import admin
from department.models import Department
from fabricator.models import Fabricator
from team.models import Team
from core.models import Staff


class DepartmentAdminModel(admin.ModelAdmin):
    def get_fab_count(self, obj):
        return Fabricator.objects.filter(department=obj).count()
    get_fab_count.short_description = 'No. of Fabricators'

    def get_staff_count(self, obj):
        return Staff.objects.filter(department=obj).count()
    get_staff_count.short_description = 'No. of Staffs'

    def get_team_count(self, obj):
        return Team.objects.filter(department=obj).count()
    get_team_count.short_description = 'No. of Teams'

    list_display = ['name', 'manager',
            'get_fab_count',
            'get_team_count',
            'get_staff_count']
    search_fields = ['name']
    list_filter = ['name']
    ordering = ['name']
    list_per_page = 10
    fieldsets =[
        ('Department', {'fields': ['name', 'manager']}),
    ]

admin.site.register(Department, DepartmentAdminModel)