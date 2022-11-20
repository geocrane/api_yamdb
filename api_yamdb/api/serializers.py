from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Review, Comment, User


class CurrentTitleIdDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs['title_id']

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(required=True)
    # email = serializers.EmailField(required=True)

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError(
                "Имя 'me' недопустимо - сериализатор"
            )
        return data

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

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
        )
        read_only_fields = ("role",)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    genre = serializers.CharField(required=True)

    class Meta:
        fields = ('name', 'slug', )
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(), many=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category')
        model = Title

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            raise serializers.ValidationError(
                'Выберите жанр!')
        title = Title.objects.create(**validated_data)
        return title

    """def validate_genre(self, value):
        if value.id is None:
            raise serializers.ValidationError('Проверьте жанр')
        return value"""

    """def validate(self, data):
        for data['genre'] in genre:
            if genre is None:
                raise serializers.ValidationError(
                'Имя не может совпадать с цветом!')
            return data"""


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
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
