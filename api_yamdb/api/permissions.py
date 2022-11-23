from rest_framework import permissions


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


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.auth:
            return False
        return True


class AuthorOrReviewerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.auth:
            return request.method in permissions.SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
