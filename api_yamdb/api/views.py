from django.contrib.auth.tokens import default_token_generator
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
    AuthorOrReadOnly,
    ModeratorAndAdminPermissions,
    AuthorOrReviewerOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    RoleReadOnly,
    ReviewSerializer,
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
        username = request.data.get("username")
        email = request.data.get("email")
        request_data = dict(username=username, email=email)
        user = User.objects.filter(username=username)
        if user and (user[0].email == email):
            user = User.objects.get(**request_data)
        else:
            SignUpSerializer(data=request.data).is_valid(raise_exception=True)
            user = User.objects.create(**request_data)
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
        GetTokenSerializer(data=request.data).is_valid(raise_exception=True)
        user = get_object_or_404(User, username=request.data.get("username"))
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
        if request.method != "PATCH":
            return Response(UserSerializer(request.user).data)
        serializer = RoleReadOnly(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg("reviews__score"))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleListSerializer
        return TitleSerializer


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReviewerOrReadOnly,)
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_title(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReviewerOrReadOnly, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs["review_id"]
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=review_id),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
