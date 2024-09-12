from rest_framework import permissions

class UpdateDeptPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.id == obj.manager.id:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
    
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return False