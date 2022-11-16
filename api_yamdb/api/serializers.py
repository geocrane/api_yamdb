"""В файле настраиваем Serializers"""

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title


class TitleSerializer(serializers.ModelSerializer):
    """to write"""

    class Meta:
        """to write"""
        fields = '__all__'
        model = Title


class CategorySerializer(serializers.ModelSerializer):
    """to write"""
    class Meta:
        """to write"""
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """to write"""
    class Meta:
        """to write"""
        fields = '__all__'
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    """ Настраиваем Serializers по модулю Review"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        """ Добавляем следующие поля из модуля Review"""
        model = Review
        title = serializers.CharField(write_only=True)
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        validators = [
        UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=['text', 'score']
        )]

    def validate_score(self, value):
        """ Проверка вводимого значения."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Введите значение от 0 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """ Настраиваем Serializers по модулю Comment"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text')

    class Meta:
        """ Добавляем следующие поля из модуля Comment"""
        model = Comment
        fields = ('id', 'text', 'review', 'author', 'pub_date',)
