from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    GetTokenAPIView,
    ReviewViewSet,
    SignUpAPIView,
    TitleViewSet,
    UserViewSet,
)

app_name = "api"

v1_router = DefaultRouter()
v1_router.register("users", UserViewSet, basename="users")
v1_router.register(r"titles", TitleViewSet, basename="titles")
v1_router.register(r"genres", GenreViewSet, basename="genres")
v1_router.register(r"categories", CategoryViewSet, basename="categories")
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

auth_routes = [
    path("auth/signup/", SignUpAPIView.as_view(), name="signup"),
    path("auth/token/", GetTokenAPIView.as_view(), name="token"),
]

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("v1/", include(auth_routes)),
]
