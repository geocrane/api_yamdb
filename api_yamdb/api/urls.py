"""Настраваем URL и роутеры."""
from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)
from django.urls import include, path
from rest_framework import routers


v1_router = routers.DefaultRouter()
v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'comments', CommentViewSet, basename='comments')
v1_router.register(r'reviews', ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
