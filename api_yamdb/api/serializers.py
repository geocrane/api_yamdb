from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Review, Comment, User


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
    class Meta:
        fields = "__all__"
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    """Настраиваем Serializers по модулю Review"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    title = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        """Добавляем следующие поля из модуля Review"""

        model = Review
        fields = (
            "id",
            "title",
            "text",
            "score",
            "author",
            "pub_date",
        )

    validators = [
        UniqueTogetherValidator(
            queryset=Review.objects.all(), fields=["title", "author"]
        )
    ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["name", "slug"]
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if not data["genre"]:
            raise serializers.ValidationError(
                "Выберите жанр"
            )
        return data
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

    # def create(self, validated_data):
    #     if 'genre' not in self.initial_data:
    #         raise serializers.ValidationError(
    #             'Выберите жанр!')
    #     title = Title.objects.create(**validated_data)
    #     return title


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title

    def get_rating(self, obj):
        return obj.rating


class CommentSerializer(serializers.ModelSerializer):
    """Настраиваем Serializers по модулю Comment"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    review = serializers.SlugRelatedField(read_only=True, slug_field="text")

    class Meta:
        """Добавляем следующие поля из модуля Comment"""

        model = Comment
        fields = (
            "id",
            "text",
            "review",
            "author",
            "pub_date",
        )
