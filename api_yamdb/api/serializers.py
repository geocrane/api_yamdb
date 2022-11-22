import datetime as dt

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title, User

from .validators import validate_username, is_email_exist, is_user_exist, validate_year


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=[validate_username, is_user_exist]
    )
    email = serializers.EmailField(validators=[is_email_exist])


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[validate_username])


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        validate_username(value)
        return value

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


class RoleReadOnly(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(), fields=["name", "slug"]
            )
        ]

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Заполните поля")
        return data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre
        validators = [
            UniqueTogetherValidator(
                queryset=Genre.objects.all(), fields=["name", "slug"]
            )
        ]

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Заполните поля")
        return data


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category")
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(), fields=["name", "year"]
            )
        ]

    def validate_year(self, value):
        year = dt.date.today().year
        if not 0 <= value <= year:
            raise serializers.ValidationError("Проверьте год!")
        return value

    def validate(self, data):
        if not data.get("category"):
            raise serializers.ValidationError("Выберите категорию!")
        if not data:
            raise serializers.ValidationError("Заполните поля")
        return data


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def get_rating(self, obj):
        return obj.rating


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError("Оцените от 0 до 10!")
        return value

    def validate(self, data):
        if self.context["request"].method != "POST":
            return data
        author = self.context["request"].user
        title_id = self.context["view"].kwargs.get("title_id")
        if Review.objects.filter(author=author, title__id=title_id).exists():
            raise serializers.ValidationError(
                "Нельзя оставлять больше одного отзыва"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "author",
            "pub_date",
        )
