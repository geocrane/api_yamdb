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
v1_router.register("users", UserViewSet, basename="user")
v1_router.register(r"titles", TitleViewSet)
v1_router.register(r"genres", GenreViewSet)
v1_router.register(r"categories", CategoryViewSet)
v1_router.register(r"comments", CommentViewSet, basename="comments")
v1_router.register(r"reviews", ReviewViewSet, basename="reviews")
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)


urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path(
        "v1/auth/signup/",
        SignUpAPIView.as_view(),
        name="signup",
    ),
    path(
        "v1/auth/token/",
        GetTokenAPIView.as_view(),
        name="token_obtain_pair",
    ),
]
