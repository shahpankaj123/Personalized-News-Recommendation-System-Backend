from rest_framework import permissions

from .permissions import AdminUserPermission,StaffUserPermission
from rest_framework.authentication import TokenAuthentication

class AdminUserPermissionMixin:
    permission_classes = [permissions.IsAuthenticated, AdminUserPermission]
    authentication_classes = [TokenAuthentication]


class StaffUserPermissionMixin:
    permission_classes = [permissions.IsAuthenticated, StaffUserPermission]    