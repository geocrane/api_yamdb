from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Title, Review, Comment
from django.db.models import Avg
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .serializers import (TitleSerializer, GenreSerializer, CategorySerializer,
                          ReviewSerializer, CommentSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year')
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Review.objects.all().annotate(_average_score=Avg(
                                             'review__score'))


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    pagination_class = LimitOffsetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """ Настройка отображения по модели Review"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def get_title(self):
        """ Получаем произведения."""
        title_id = self.kwargs.get('title_id ')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().review.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """ Настройка отображения по модели Comment"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()
