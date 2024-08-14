from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import Client, BaseUser

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
class ClientUserModel(BaseUserModel):
    form = ClientUserForm

    def get_fabricator_name(self, obj):
        return obj.fabricator.name
    get_fabricator_name.short_description = 'Fabricator'

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


admin.site.register(Client, ClientUserModel)
admin.site.register(BaseUser, BaseUserModel)