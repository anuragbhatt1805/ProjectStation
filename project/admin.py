from django.contrib import admin
from project.models import (
    Project,
    ProjectComment,
    ProjectFile,
    Feedback
)

class ProjectCommentInline(admin.TabularInline):
    model = ProjectComment
    extra = 0
    readonly_fields = ['added_by', 'added_on']
    fields = ['comment', 'file', 'tags', 'added_by', 'added_on']
    
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

    def get_file_count(self, obj):
        return obj.get_all_file().count()
    get_file_count.short_description = 'File Attached'

    list_display = ['name', 'fabricator', 'department', 'team', 'manager', 'status', 'stage', 'get_file_count']
    list_filter = ['fabricator', 'department', 'team', 'manager', 'status', 'stage']
    search_fields = ['name', 'fabricator', 'department', 'team', 'manager', 'status', 'stage    ']
    list_max_show_all = 10
    fieldsets = [
        ('Project Information', {
            'fields' : ['name', 'description', ]
        }),
        ('Project Stage & Status', {
            'fields' : ['status', 'stage']
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
        ('Additional Information', {
            'fields' : ['tool', 'connectionDesign', 'miscDesign', 'customerDesign']
        }),
        ('Important Dates', {
            'fields' : ['start_date', 'approval_date']
        }),
        ('Delete', {
            'fields':['is_bin'],
            'classes':['collapse']
        })
    ]

class FeedbackModelAdmin(admin.ModelAdmin):
    def get_project_name(self, obj):
        return obj.project.name
    get_project_name.short_description = 'Project Name'

    def get_employee_name(self, obj):
        return obj.client.full_name()
    get_employee_name.short_description = 'Client Name'

    list_display = ['get_project_name', 'get_employee_name', 'rating', 'feedback']
    list_filter = ['project__name', 'project__fabricator', 'rating']
    search_fields = ['project', 'feedback']
    ordering = ['project', 'rating']
    fieldsets = [
        ('Project Information', {
            'fields' : ['project',]
        }),
        ('Client Information', {
            'fields' : ['client']
        }),
        ('Feedback Information', {
            'fields' : ['feedback', 'rating']
        }),
    ]

admin.site.register(Project, ProjectModelAdmin)
admin.site.register(Feedback, FeedbackModelAdmin)