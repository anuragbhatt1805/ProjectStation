from django.contrib import admin
from project.models import (
    Project,
    ProjectComment,
    ProjectFile
)

class ProjectCommentInline(admin.TabularInline):
    model = ProjectComment
    extra = 0
    readonly_fields = ['added_by', 'added_on']
    fields = ['comment', 'file', 'added_by', 'added_on']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['project']
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        obj.save()

class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 0
    readonly_fields = ['added_by', 'added_on']
    fields = [ 'file', 'added_by', 'added_on']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['project']
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        obj.save()

class ProjectModelAdmin(admin.ModelAdmin):
    inlines = [ProjectCommentInline, ProjectFileInline]
    list_display = ['name', 'fabricator', 'department', 'team', 'manager', 'status']
    list_filter = ['fabricator', 'department', 'team', 'manager', 'status']
    search_fields = ['name', 'fabricator', 'department', 'team', 'manager', 'status']
    list_max_show_all = 10
    fieldsets = [
        ('Project Information', {
            'fields' : ['name', 'status', 'stage']
        }),
        ('Department Information', {
            'fields' : ['department', 'manager']
        }),
        ('Fabricator Information', {
            'fields' : ['fabricator',]
        }),
        ('Team Information', {
            'fields' : ['team',]
        }),
        ('Important Dates', {
            'fields' : ['start_date', 'approval_date']
        }),
    ]

admin.site.register(Project, ProjectModelAdmin)