from rest_framework import permissions

from .permissions import AdminUserPermission,AdminStaffUserPermission
from rest_framework.authentication import TokenAuthentication

class AdminUserPermissionMixin:
    permission_classes = [permissions.IsAuthenticated, AdminUserPermission]
    authentication_classes = [TokenAuthentication]


class AdminStaffUserPermissionMixin:
    permission_classes = [permissions.IsAuthenticated, AdminStaffUserPermission] 
    authentication_classes = [TokenAuthentication]   