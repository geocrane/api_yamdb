""" Настройка отображения ViewSet"""

from django.shortcuts import get_object_or_404
from api.permissions import IsUserOrReadOnly
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from reviews.models import Comment, Review, Title
from api.serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ Настройка отображения по модели Review"""
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=review_id)
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
