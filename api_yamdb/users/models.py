
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
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

    def my_view(request):
        try:
            user = MyModel.objects.get(pk=1)
        except MyModel.DoesNotExist:
            raise Http404("No MyModel matches the given query.")


class User(AbstractUser):
    bio = models.TextField(default=None, null=True)
    role = models.CharField(max_length=255, default="user", null=True)

    def __str__(self):
        return self.email