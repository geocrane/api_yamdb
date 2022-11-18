from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsUserOrReadOnly(BasePermission):
    """ Настраиваем уровень разрешения в зависимости от авторизации
    и автора. Только автор может корректировать свои записи.
    Аторизованный пользователь может только просматривать чужие записи."""
    # message = 'Изменение чужого контента запрещено!'
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user)


class IsAdminOrReadOnly(BasePermission):
    """ Настраиваем уровень разрешения в зависимости типа авторизации,
    Анонимный и авторизованный пользователь видят текущую запись.
    Возможность удаления есть только у админа."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsModeratorOrReadOnly(BasePermission):
    """ Настраиваем уровень разрешения модер,
    Возможно смотреть редактировать свои записи.
    Дополнительно право право удалять и редактировать
    любые отзывы и комментарии. """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_moderator
            and request.user.is_authenticated
        )
