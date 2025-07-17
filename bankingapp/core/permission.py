from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsBanker(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'BANKER'

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'CLIENT'
