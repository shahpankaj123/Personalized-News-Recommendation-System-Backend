from rest_framework.permissions import BasePermission
from .models import User

class AdminUserPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return bool(False)
        if request.user is None:
            return bool(False)
        user_type = User.objects.get(email=request.user)
        print(user_type)
        if user_type.is_admin:
            return bool(True)
        return bool(False)
    
class StaffUserPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return bool(False)
        if request.user is None:
            return bool(False)
        user_type = User.objects.get(email=request.user)
        if user_type.is_staffusers:
            return bool(True)
        return bool(False)    