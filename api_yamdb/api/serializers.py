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


class NotAdminSerializer(serializers.ModelSerializer):
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
        read_only_fields = ("role",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Genre


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


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
            "review",
        )
        model = Title

    def get_rating(self, obj):
        return obj.rating

    def validate_score(self, value):
        """Проверка возможности подписки на себя."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Введите значение от 0 до 10!")
        return value


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
