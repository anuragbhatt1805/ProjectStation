from django.contrib import admin
from team.models import Team, Member


class MemberInline(admin.TabularInline):
    model = Member
    extra = 0
    fields = ('employee', 'role')


class TeamAdmin(admin.ModelAdmin):
    inlines = [MemberInline]

    def get_member_count(self, obj):
        return obj.get_members_count()
    get_member_count.short_description = 'No of Team Members'

    list_display = ('name', 'department', 'leader', 'get_member_count')
    list_filter = ('department__name', 'leader')
    search_fields = ('name', 'department', 'leader')
    ordering = ['name']
    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'leader')
        }),
        ('Department Information', {
            'fields': ('department', )
        }),
        ('Delete', {
            'fields':['is_bin'],
            'classes':['collapse']
        })
    )


class MemberAdmin(admin.ModelAdmin):
    def get_team_name(self, obj):
        return obj.team.name
    get_team_name.short_description = 'Team'

    def get_employee_name(self, obj):
        return obj.employee.username
    get_employee_name.short_description = 'Employee'

    list_display = ('id', 'team', 'role', 'employee')
    list_filter = ['team__name', 'role']
    search_fields = ('employee', 'team')
    ordering = ['id', 'team', 'employee']
    fieldsets = [
        ('Team Information', {
            'fields': ('team',)
        }),
        ('Member Information', {
            'fields': ('role', 'employee')
        }),
    ]


admin.site.register(Team, TeamAdmin)
admin.site.register(Member, MemberAdmin)
