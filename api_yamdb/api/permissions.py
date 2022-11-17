from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):
    # """ Настраиваем уровень разрешения в зависимости от авторизации
    # и автора. Только автор может корректировать свои записи.
    # Аторизованный пользователь может только просматривать чужие записи."""

    # message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)
