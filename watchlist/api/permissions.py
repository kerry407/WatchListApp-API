from math import perm
from rest_framework import permissions 

class AdminOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or request.user.is_staff 
        )
        
class ReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            obj.created_by == request.user 