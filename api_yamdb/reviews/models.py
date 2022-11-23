from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year, validate_username

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"
ROLES = [(USER, USER), (MODERATOR, MODERATOR), (ADMIN, ADMIN)]


class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, validators=[validate_username]
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, default="")
    last_name = models.CharField(max_length=150, default="")
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff or self.role == ADMIN

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
    pass


class Genre(BaseDescription):
    pass


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
        validators=[MaxValueValidator(10), MinValueValidator(1)],
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
