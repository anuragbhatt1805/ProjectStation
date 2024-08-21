from django.contrib import admin
from task.models import (
    Task,
    TaskComment,
    TaskFile,
    AssignedList
)
from datetime import datetime

class AssignedListInline(admin.TabularInline):
    model = AssignedList
    extra = 0
    readonly_fields = ('assigned_by', 'approved_by', 'approved_on', 'assigned_on')
    fields = ('assigned_to', 'approved', 'comment', 'assigned_on', 'approved_by', 'approved_on')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('task',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.assigned_by = request.user
        obj.save()

class TaskFileInline(admin.TabularInline):
    model = TaskFile
    extra = 0
    readonly_fields = ('added_by', 'added_on')
    fields = ('file', 'added_by', 'added_on')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('task',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        obj.save()

class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 0
    readonly_fields = ('added_by', 'added_on')
    fields = ('comment', 'file', 'tags', 'added_by', 'added_on')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('task',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        obj.save()

class TaskModelAdmin(admin.ModelAdmin):
    inlines = [AssignedListInline, TaskFileInline, TaskCommentInline]

    def get_file_count(self, obj):
        return obj.get_all_file().count()
    get_file_count.short_description = 'File Attached'

    def get_child_task(self, obj):
        return obj.get_child_tasks().count()
    get_child_task.short_description = 'Child Task'

    def get_child_tasks_display(self, obj):
        child_tasks = obj.get_child_tasks()
        if child_tasks.exists():
            return ', '.join([task.name for task in child_tasks])
        else:
            return '-'
    get_child_tasks_display.short_description = 'Child Tasks'

    list_display = ['name', 'project', 'status', 'priority', 'user', 'get_file_count', 'get_child_task']
    list_filter = ['project__fabricator', 'project__name', 'user', 'status', 'priority',]
    search_fields = ['name', 'user', 'status', 'project']
    list_max_show_all = 10
    readonly_fields = ['created_by', 'created_on', 'get_child_tasks_display']
    fieldsets = [
        ('Task Information', {
            'fields' : ['name', 'description',]
        }),
        ('Project Information', {
            'fields':['project',]
        }),
        ('Task Tree', {
            'classes': ('wide',),
            'fields': [
                'parent', 'get_child_tasks_display'
            ]
        }),
        ('Task Status & Priority', {
            'fields' : ['status', 'priority']
        }),
        ('User Information', {
            'fields' : ['user', 'created_by']
        }),
        ('Important Date', {
            'fields' : ['duration', 'due_date']
        }),
        ('Delete', {
            'fields':['is_bin'],
            'classes':['collapse']
        })
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.save()
            obj.add_assignes(
                assigned_by=request.user,
                assigned_to=form.cleaned_data['user'],
                approved_by=request.user,
                approved_on=datetime.now(),
                approved=True,
                comment="First Assignee"
            )
        obj.save()

admin.site.register(Task, TaskModelAdmin)