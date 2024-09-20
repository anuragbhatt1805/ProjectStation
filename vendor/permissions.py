from rest_framework import permissions
from core.models import VendorUser

class UpdateVendorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        vendor = VendorUser.objects.get(pk=request.user.id)
        if vendor.vendor.id == obj.id:
            return True
        return False
    
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return False