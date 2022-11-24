from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User,
    USERNAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
)
from reviews.validators import validate_year, validate_username


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username],
    )
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH
    )


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username],
        required=True,
    )
    confirmation_code = serializers.CharField(max_length=None, required=True)


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

    def validate_username(self, value):
        return validate_username(value)


class RoleReadOnly(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category")
        model = Title


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title

        fields = (
            "id", "name", "year", "genre",
            "category", "description", "rating"
        )
        read_only_fields = (
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")

    def validate(self, data):
        request = self.context["request"]
        if request.method != "POST":
            return data
        title_id = self.context.get("view").kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(title=title, author=request.user).exists():
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
