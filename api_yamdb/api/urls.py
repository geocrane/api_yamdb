from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    CommentViewSet,
    ReviewViewSet,
    UserViewSet
)

v1_router = DefaultRouter()
v1_router.register("users", UserViewSet, basename="user")
v1_router.register(r"titles", TitleViewSet)
v1_router.register(r"genres", GenreViewSet)
v1_router.register(r"categories", CategoryViewSet)
v1_router.register(r"comments", CommentViewSet, basename="comments")
v1_router.register(r"reviews", ReviewViewSet, basename="reviews")
# v1_router.register(
#     r'title/(?P<title_id>\d+)/reviews', CommentViewSet, basename='comments')


urlpatterns = [
    path("v1/", include(v1_router.urls)),
]
