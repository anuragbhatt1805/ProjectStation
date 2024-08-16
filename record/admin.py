from django.contrib import admin
from record.models import (
    PushRecord,
    TaskRecord
)

class PushRecordInline(admin.TabularInline):
    model = PushRecord
    extra = 0
    readonly_fields = ['timestamp', ]
    fields = ['type', 'timestamp', ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['record']
        return self.readonly_fields

class RecordAdmin(admin.ModelAdmin):

    inlines = [PushRecordInline, ]
    
    def get_total_time(self, obj):
        time = obj.get_total_time()
        hrs = int(time / 3600)
        mint = int((time % 3600) / 60)
        sec = int((time % 3600) % 60)
        return f'{hrs}:{mint}:{sec}'
    get_total_time.short_description = 'Total Time Taken'

    def task_duration(self, obj):
        return obj.task.duration
    task_duration.short_description = 'Assigned Time'
    
    list_display = ['task', 'user', 'get_total_time', 'task_duration']
    search_fields = ['task', 'user']
    list_filter = ['task', 'user']

admin.site.register(TaskRecord, RecordAdmin)