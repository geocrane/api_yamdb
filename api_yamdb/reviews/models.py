import datetime
from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(null=True, max_length=128)
    bio = models.TextField(null=True)
    role = models.CharField(max_length=255, default="user", null=True)

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField("Категория", max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return {self.name}


class Genre(models.Model):
    name = models.CharField("Жанр", max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return {self.name}


class Title(models.Model):
    name = models.CharField("Название", max_length=256)
    year = models.IntegerField(
        "Год выпуска",
        validators=[
            MaxValueValidator(datetime.datetime.now().year),
            MinValueValidator(0),
        ],
        default=1900
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name="titles")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="titles"
    )

    @property
    def rating(self):
        if hasattr(self, "_rating"):
            return self._rating
        return self.review.aggregate(Avg("score"))


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        "Дата публикации отзыва", auto_now_add=True, db_index=True
    )


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата публикации комментария", auto_now_add=True, db_index=True
    )


# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None):
#         if username is None:
#             raise TypeError("Поле username - обязательное")
#         if email is None:
#             raise TypeError("Поле email - обязательное")
#      user = self.model(username=username, email=self.normalize_email(email))
#         user.set_password(password)
#         user.save()
#         return user
#     def create_superuser(self, username, email, password):
#         if password is None:
#             raise TypeError("Пароль суперпользователя - обязателен")
#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
#         return user
