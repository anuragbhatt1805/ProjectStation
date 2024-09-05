from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import Staff, Client, VendorUser, BaseUser

class BaseUserModel(BaseUserAdmin):
    def get_full_name(self, obj):
        return obj.full_name()
    get_full_name.short_description = 'Full Name'

    ordering = ['username',]
    list_display = ['username', 'get_full_name', 'phone', 'email', 'role', 'is_active']
    search_fields = ['username', 'f_name', 'm_name', 'l_name', 'phone']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser']
    readonly_fields = ['last_login',]
    list_max_show_all = 10
    fieldsets = [
        ('User Information', {
            'fields': ['username', 'f_name', 'm_name', 'l_name'],
            'classes': ['wide']
        }),
        ('Contact Information', {
            'fields': ['phone', 'email'],
            'classes': ['wide']
        }),
        ('Role Information', {
            'fields': ['role', 'is_active', 'is_staff', 'is_superuser'],
            'classes' : ['wide']
        }),
        ('Important Dates', {
            'fields': ['last_login',],
            'classes': ['collapse']
        }),
        ('Security', {
            'fields': ['password'],
            'classes': ['collapse']
        })
    ]
    add_fieldsets = [
        ('User Information', {
            'fields': ['username', 'f_name', 'm_name', 'l_name'],
            'classes': ['wide']
        }),
        ('Contact Information', {
            'fields': ['phone', 'email'],
            'classes': ['wide']
        }),
        ('Role Information', {
            'fields': ['role', 'is_active', 'is_staff', 'is_superuser'],
            'classes' : ['wide']
        }),
        ('Security', {
            'fields': ['password1', 'password2'],
            'classes': ['wide']
        })
    ]

class ClientUserForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # instance is None when adding a new object
            self.fields['role'].initial = 'CLIENT'

class ClientUserModel(BaseUserAdmin):
    form = ClientUserForm

    def get_full_name(self, obj):
        return obj.full_name()
    get_full_name.short_description = 'Full Name'

    list_display = ['username', 'get_full_name', 'fabricator', 'phone', 'email', 'is_active']
    search_fields = ['username', 'fabricator', 'f_name', 'm_name', 'l_name', 'phone']
    list_filter = ['fabricator__name', 'is_active', ]
    readonly_fields = ['last_login', 'role']
    list_max_show_all = 10
    fieldsets = [
        ('User Information', {
            'fields': ['username', 'f_name', 'm_name', 'l_name'],
            'classes': ['wide']
        }),
        ('User Fabricator Details', {
            'fields':['fabricator', 'designation', 'address', 'city', 'state', 'country', 'zip_code'],
            'classes':['wide']
        }),
        ('Contact Information', {
            'fields': ['email', 'phone', 'alt_phone'],
            'classes': ['wide']
        }),
        ('Role Information', {
            'fields': ['role', 'is_active', ],
            'classes' : ['wide']
        }),
        ('Important Dates', {
            'fields': ['last_login',],
            'classes': ['collapse']
        }),
        ('Security', {
            'fields': ['password'],
            'classes': ['collapse']
        })
    ]
    add_fieldsets = [
        ('User Information', {
            'fields': ['username', 'f_name', 'm_name', 'l_name'],
            'classes': ['wide']
        }),
        ('User Fabricator Details', {
            'fields':['fabricator', 'designation', 'address', 'city', 'state', 'country', 'zip_code'],
            'classes':['wide']
        }),
        ('Contact Information', {
            'fields': ['email', 'phone', 'alt_phone'],
            'classes': ['wide']
        }),
        ('Role Information', {
            'fields': ['is_active', 'role'],
            'classes' : ['wide']
        }),
        ('Security', {
            'fields': ['password1', 'password2'],
            'classes': ['wide']
        })
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # if the object is being created
            obj.role = 'CLIENT'
        super().save_model(request, obj, form, change)

class StaffUserForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # instance is None when adding a new object
            self.fields['role'].initial = 'STAFF'

class StaffUserModel(BaseUserAdmin):
    form = StaffUserForm

    def get_full_name(self, obj):
        return obj.full_name()
    get_full_name.short_description = 'Full Name'

    list_display = ['username', 'get_full_name', 'department', 'phone', 'email', 'is_active']
    search_fields = ['username', 'department', 'f_name', 'm_name', 'l_name', 'phone']
    list_filter = ['department__name', 'is_active', ]
    readonly_fields = ['last_login', 'role']
    list_max_show_all = 10
    fieldsets = [
        ('User Information', {
            'fields': ['username', 'f_name', 'm_name', 'l_name'],
            'classes': ['wide']
        }),
        ('User Department Details', {
            'fields':['emp_code', 'department', 'designation', 'manager', 'sales'],
            'classes':['wide']
        }),
        ('Contact Information', {
            'fields': ['email', 'phone'],
            'classes': ['wide']
        }),
        ('Role Information', {
            'fields': ['role', 'is_active', 'is_staff', 'is_superuser'],
            'classes' : ['wide']
        }),
        ('Important Dates', {
            'fields': ['last_login',],
            'classes': ['collapse']
        }),
        ('Security', {
            'fields': ['password'],
            'classes': ['collapse']
        })
    ]
    add_fieldsets = [
        ('User Information', {
            'fields': ['username', 'f_name', 'm_name', 'l_name'],
            'classes': ['wide']
        }),
        ('User Department Details', {
            'fields':['emp_code', 'department', 'designation', 'manager', 'sales'],
            'classes':['wide']
        }),
        ('Contact Information', {
            'fields': ['email', 'phone' ],
            'classes': ['wide']
        }),
        ('Role Information', {
            'fields': ['role', 'is_active', 'is_staff', 'is_superuser'],
            'classes' : ['wide']
        }),
        ('Security', {
            'fields': ['password1', 'password2'],
            'classes': ['wide']
        })
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # if the object is being created
            obj.role = 'STAFF'
        super().save_model(request, obj, form, change)

class VendorUserForm(forms.ModelForm):
    class Meta:
        model = VendorUser
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # instance is None when adding a new object
            self.fields['role'].initial = 'VENDOR'

class VendorUserModel(BaseUserAdmin):
    form = VendorUserForm

    def get_full_name(self, obj):
        return obj.full_name()
    get_full_name.short_description = 'Full Name'

    list_display = ['username', 'get_full_name', 'vendor', 'phone', 'email', 'is_active']
    search_fields = ['username', 'f_name', 'm_name', 'l_name', 'phone', 'email', 'vendor', 'title']
    list_filter = ['is_active', 'vendor__name']
    readonly_fields = ['last_login', 'role']
    list_max_show_all = 10
    fieldsets = [
        ('User Information', {
            'fields': ['username', 'f_name', 'm_name', 'l_name'],
            'classes': ['wide']
        }),
        ('Vendor Information', {
            'fields': ['vendor', 'title'],
            'classes': ['wide']
        }),
        ('Contact Information', {
            'fields': ['phone', 'email'],
            'classes': ['wide']
        }),
        ('Role Information', {
            'fields': ['role', 'is_active', 'contactPoint'],
            'classes' : ['wide']
        }),
        ('Important Dates', {
            'fields': ['last_login',],
            'classes': ['collapse']
        }),
        ('Security', {
            'fields': ['password'],
            'classes': ['collapse']
        })
    ]
    add_fieldsets = [
        ('User Information', {
            'fields': ['username', 'f_name', 'm_name', 'l_name'],
            'classes': ['wide']
        }),
        ('Vendor Information', {
            'fields': ['vendor', 'title'],
            'classes': ['wide']
        }),
        ('Contact Information', {
            'fields': ['phone', 'email'],
            'classes': ['wide']
        }),
        ('Role Information', {
            'fields': ['role', 'is_active', 'contactPoint'],
            'classes' : ['wide']
        }),
        ('Security', {
            'fields': ['password1', 'password2'],
            'classes': ['wide']
        })
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # if the object is being created
            obj.role = 'VENDOR'
        super().save_model(request, obj, form, change)

admin.site.register(Staff, StaffUserModel)
admin.site.register(Client, ClientUserModel)
admin.site.register(BaseUser, BaseUserModel)
admin.site.register(VendorUser, VendorUserModel)
