from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title, User
from .filters import TitleFilter
from .permissions import (
    AdminOrReadOnly,
    AdminPermissions,
    AuthorOrReviewerOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    RoleReadOnly,
    SignUpSerializer,
    TitleListSerializer,
    TitleSerializer,
    UserSerializer,
)

CONFIRMATION_MESSAGE = "Ваш логин {user}, код подтверждения {token}"
CONFIRMATION_IS_NOT_MATCH = "Пользователь и код подтверждения - не совпадают"


class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
            )
        except IntegrityError:
            return Response(
                "Логин или email используются другим пользователем",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.email_user(
            "Confirmation code",
            CONFIRMATION_MESSAGE.format(
                user=user.username,
                token=default_token_generator.make_token(user),
            ),
        ),
        return Response(request.data, status=status.HTTP_200_OK)


class GetTokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data.get("username")
        )
        if not default_token_generator.check_token(
            user, request.data.get("confirmation_code")
        ):
            return Response(
                CONFIRMATION_IS_NOT_MATCH,
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
            }
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AdminPermissions,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    pagination_class = LimitOffsetPagination
    lookup_field = "username"

    @action(
        methods=["get", "patch"],
        url_path="me",
        permission_classes=(IsAuthenticated,),
        detail=False,
    )
    def get_self_user(self, request):
        if request.method == "GET":
            return Response(UserSerializer(request.user).data)
        serializer = RoleReadOnly(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg("reviews__score"))
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)
    ordering = ("rating", "name")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleListSerializer
        return TitleSerializer


class BaseDescriptionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(BaseDescriptionViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(BaseDescriptionViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReviewerOrReadOnly,)
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReviewerOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
