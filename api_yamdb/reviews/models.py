"""to write"""
import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Category(models.Model):
    """to write"""
    name = models.CharField(
        'Категория',
        max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    def __str__(self):
        return str({self.name})


class Genre(models.Model):
    """to write"""
    name = models.CharField(
        'Жанр',
        max_length=256)
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return str({self.name})


class Title(models.Model):
    """to write"""
    name = models.CharField(
        'Название',
        max_length=256
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(datetime.datetime.now().year),
                    MinValueValidator(0)]
    )

    description = models.TextField(
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )


class Review(models.Model):
    """to write"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models. IntegerField(
        validators=[MaxValueValidator(10),
                    MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )


class Comment(models.Model):
    """to write"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )
