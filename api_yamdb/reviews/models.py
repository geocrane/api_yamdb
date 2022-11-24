from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year, validate_username

USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254
FIRST_NAME_LENGTH = 150
LAST_NAME_LENGTH = 150


USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"
ROLES = [(USER, USER), (MODERATOR, MODERATOR), (ADMIN, ADMIN)]


class User(AbstractUser):
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[validate_username],
    )
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True)
    first_name = models.CharField(max_length=FIRST_NAME_LENGTH, default="")
    last_name = models.CharField(max_length=LAST_NAME_LENGTH, default="")
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username


class BaseDescription(models.Model):
    name = models.CharField("Имя", max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(BaseDescription):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(BaseDescription):
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    name = models.TextField("Название")
    year = models.IntegerField("Год выпуска", validators=[validate_year])
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name="titles")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="titles"
    )

    def __str__(self):
        return self.name


class Note(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ["-pub_date"]


class Review(Note):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
    )

    class Meta(Note.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="only_one_review",
            ),
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(Note):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )

    class Meta(Note.Meta):
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
