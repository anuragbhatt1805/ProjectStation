from typing import Any
from django.contrib import admin
from fabricator.models import Fabricator, StandardDesign

class StandardDesignInline(admin.TabularInline):
    model = StandardDesign
    extra = 0
    readonly_fields = ['added_by', 'added_on']
    fields = ['file', 'added_by', 'added_on']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + [ 'fabricator',]
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        obj.save()

class FabricatorModelAdmin(admin.ModelAdmin):
    def get_contact_count(self, obj):
        return obj.list_contact().count()
    get_contact_count.short_description = 'Contact Count'

    def get_design_count(self, obj):
        return obj.list_design().count()
    get_design_count.short_description = 'Design Count'

    inlines = [StandardDesignInline,]

    ordering = ['name', 'department']
    list_display = ['name', 'department', 'city', 'state', 'country', 'get_contact_count', 'get_design_count']
    list_filter = ['department', 'city', 'state', 'country', 'zip_code', 'is_bin']
    search_fields = ['name', 'zip_code', 'address', 'website']
    list_max_show_all = 10
    fieldsets = [
        ('Fabricator', {
            'fields' : ['name', 'department']
        }),
        ('Location', {
            'fields' : ['address', 'city', 'state', 'country', 'zip_code']
        }),
        ('Website', {
            'fields' : ['website', 'drive']
        }),
        ('Delete', {
            'fields':['is_bin'],
            'classes':['collapse']
        })
    ]

admin.site.register(Fabricator, FabricatorModelAdmin)