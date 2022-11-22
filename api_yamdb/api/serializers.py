import datetime as dt

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title, User
from django.shortcuts import get_object_or_404
from .validators import validate_username, is_email_exist, is_user_exist


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

    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category")
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not 0 <= value <= year:
            raise serializers.ValidationError("Проверьте год!")
        return value


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ("id",
                  "name",
                  "year",
                  "rating",
                  "description",
                  "genre",
                  "category")

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

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = Title.objects.filter(pk=title_id)
        if request.method == 'POST':
            if title:
                if Review.objects.filter(title=title[0], author=author):
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
