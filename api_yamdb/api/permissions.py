from rest_framework import permissions
from reviews.models import ADMIN, MODERATOR, USER


class AdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.auth:
            return False
        if request.user.is_admin or request.user.is_staff:
            return True


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.auth:
            return False
        if request.user.is_admin or request.user.is_staff:
            return True
        return False


class ModeratorPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.auth:
            return False
        if request.user.role in (MODERATOR, ADMIN):
            return True


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.auth:
            return False
        if request.user.role in (USER, MODERATOR, ADMIN):
            return True


class AuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.auth:
            if request.method in permissions.SAFE_METHODS:
                return True
            return False
        if request.user.role in (USER, MODERATOR, ADMIN):
            return True

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
