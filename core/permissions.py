from rest_framework import permissions

class UpdateProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
    
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False