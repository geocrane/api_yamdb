# import jwt

# from datetime import datetime, timedelta
# from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Поле username - обязательное')
        if email is None:
            raise TypeError('Поле email - обязательное')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Пароль суперпользователя - обязателен')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return self.email

    # def _generate_jwt_token(self):
    #     """
    #     Генерирует веб-токен JSON, в котором хранится идентификатор этого
    #     пользователя, срок действия токена составляет 1 день от создания
    #     """
    #     dt = datetime.now() + timedelta(days=1)
    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')
    #     return token.decode('utf-8')
