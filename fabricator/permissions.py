from rest_framework import permissions
from core.models import Client

class UpdateFabPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        client = Client.objects.get(pk=request.user.id)
        if client.fabricator.id == obj.id:
            return True
        return False
    
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return False