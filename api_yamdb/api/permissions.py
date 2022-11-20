""" Настравиваем уровни доступа."""
from rest_framework import permissions


class UserPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == "user"


class ModeratorPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user.role == "Модератор")


class IsAdminOrReadOnly(permissions.BasePermission):
    """ Настраиваем уровень разрешения в зависимости типа авторизации,
    Анонимный и авторизованный пользователь видят текущую запись.
    Возможность удаления есть только у админа."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsUserOrReadOnly(permissions.BasePermission):
    """ Настраиваем уровень разрешения в зависимости от авторизации
    и автора. Только автор может корректировать свои записи.
    Аторизованный пользователь может только просматривать чужие записи."""

    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)
