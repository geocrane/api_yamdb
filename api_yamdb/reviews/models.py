import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"
ROLES = [(USER, USER), (MODERATOR, MODERATOR), (ADMIN, ADMIN)]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(default="", max_length=128)
    bio = models.TextField(null=True)
    role = models.CharField(
        max_length=255, choices=ROLES, default=USER, null=True
    )

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField("Категория", max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField("Жанр", max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField("Название", max_length=256)
    year = models.IntegerField(
        "Год выпуска",
        validators=[
            MaxValueValidator(datetime.datetime.now().year),
            MinValueValidator(0),
        ],
        default=1900,
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name="titles")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="titles"
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10), MinValueValidator(0)],
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="only_one_review",
            ),
        ]


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
