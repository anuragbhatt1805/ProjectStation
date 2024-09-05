from django.contrib import admin
from vendor.models import Vendor, VendorDesign

class VendorDesignInline(admin.TabularInline):
    model = VendorDesign
    extra = 0
    readonly_fields = ['added_by', 'added_on']
    fields = ['file', 'added_by', 'added_on']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + [ 'vendor',]
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        obj.save()


class VendorModelAdmin(admin.ModelAdmin):

    def get_user_count(self, obj):
        return obj.list_all_user().count()
    get_user_count.short_description = 'User Count'

    def get_design_count(self, obj):
        return obj.list_design().count()
    get_design_count.short_description = 'Design Count'

    inlines = [VendorDesignInline,]

    ordering = ['name', ]
    list_display = ['name',   'city', 'state', 'country', 'get_design_count', 'get_user_count']
    list_filter = [  'city', 'state', 'country', 'zip_code', 'is_bin']
    search_fields = ['name', 'zip_code']
    list_max_show_all = 10
    fieldsets = [
        ('Vendor', {
            'fields' : ['name',  ]
        }),
        ('Location', {
            'fields' : ['city', 'state', 'country', 'zip_code']
        }),
        ('Delete', {
            'fields':['is_bin'],
            'classes':['collapse']
        })
    ]


admin.site.register(Vendor, VendorModelAdmin)