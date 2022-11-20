""" Настравиваем уровни доступа."""
from rest_framework import permissions

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"


class AdminPermissions(permissions.BasePermission):
    """ Настраиваем уровень разрешения в зависимости типа авторизации,
    Анонимный и авторизованный пользователь видят текущую запись.
    Возможность удаления есть только у админа."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.auth:
            return False
        if request.user.role in (ADMIN,) or request.user.is_staff:
            return True
        return False


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.auth:
            return False
        if request.user.role in (USER, MODERATOR, ADMIN):
            return True

class ModeratorPermissions(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if  obj.author == request.user:
            return True
        if not request.auth:
            return False
        if request.user.role in (MODERATOR, ADMIN):
            return True

    
    # def has_object_permission(self, request, view, obj):
    #     return (
    #         request.method in permissions.SAFE_METHODS
    #         or obj.author == request.user)


class IsUserOrReadOnly(permissions.BasePermission):
    """ Настраиваем уровень разрешения в зависимости от авторизации
    и автора. Только автор может корректировать свои записи.
    Аторизованный пользователь может только просматривать чужие записи  ."""

    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)
