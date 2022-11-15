import datetime
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


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
    year = (
        models.IntegerField(
            "Год выпуска",
            validators=[
                MaxValueValidator(datetime.date.today().year),
                MinValueValidator(0),
            ],
        ),
    )
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre, related_name="titles"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="titles"
    )


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
