from rest_framework import permissions


class AdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.auth:
            return False
        return request.user.is_admin


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.auth and request.user.is_admin
        ) or request.method in permissions.SAFE_METHODS


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
