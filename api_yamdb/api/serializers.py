import datetime as dt
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Review, Comment, User


class SignUpSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data.get("username") == "me":
            raise serializers.ValidationError(
                "Имя 'me' недопустимо"
            )
        return data

    class Meta:
        model = User
        fields = ["username", "email"]


class GetTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class NotRoleChanging(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )


class CategorySerializer(serializers.ModelSerializer):
    """ Настраиваем Serializers по модулю Category"""

    class Meta:
        """ Добавляем следующие поля из модуля Category"""
        fields = ('name', 'slug')
        model = Category
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['name', 'slug']
            )
        ]

    def validate(self, data):
        if not data:
            raise serializers.ValidationError(
                'Заполните поля')
        return data


class GenreSerializer(serializers.ModelSerializer):
    """ Настраиваем Serializers по модулю Genre"""

    class Meta:
        """ Добавляем следующие поля из модуля Genre"""
        fields = ('name', 'slug', )
        model = Genre
        validators = [
            UniqueTogetherValidator(
                queryset=Genre.objects.all(),
                fields=['name', 'slug']
            )
        ]

    def validate(self, data):
        if not data:
            raise serializers.ValidationError(
                'Заполните поля')
        return data


class TitleSerializer(serializers.ModelSerializer):
    """ Настраиваем Serializers по модулю Title для post, patch, delete"""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(), many=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        """ Добавляем следующие поля из модуля Title"""
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category')
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['name', 'year']
            )
        ]

    def validate_year(self, value):
        """ Проверка года"""
        year = dt.date.today().year
        if not 0 <= value <= year:
            raise serializers.ValidationError('Проверьте год!')
        return value

    def validate(self, data):
        """ Проверка вводимых данных"""
        if not data.get('genre'):
            raise serializers.ValidationError(
                'Выберите жанр')
        if not data.get('category'):
            raise serializers.ValidationError(
                'Выберите категорию!')
        if not data:
            raise serializers.ValidationError(
                'Заполните поля')
        return data


class TitleListSerializer(serializers.ModelSerializer):
    """ Настраиваем Serializers по модулю Title для list, retrieve"""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        """ Добавляем следующие поля из модуля Title"""
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title

    def get_rating(self, obj):
        return obj.rating


class ReviewSerializer(serializers.ModelSerializer):
    """ Настраиваем Serializers по модулю Review"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        """ Добавляем следующие поля из модуля Review"""
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['text', 'score']
            )
        ]

    def validate_score(self, value):
        """ Проверка вводимого значения диапазон чисел."""
        if not (1 <= value <= 10):
            raise serializers.ValidationError('Оцените от 0 до 10!')
        return value

    def validate(self, data):
        """ Проверяем, что На одно произведение пользователь
        может оставить только один отзыв. """
        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
            author=author,
            title__id=title_id
        ).exists():
            raise serializers.ValidationError('Нельзя оставить 2 отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """ Настраиваем Serializers по модулю Comment"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        """ Добавляем следующие поля из модуля Comment"""
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
