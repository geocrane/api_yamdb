from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework import viewsets, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
)

from reviews.models import Comment, Review, Title, Category, Genre, User
from .permissions import (
    AdminPermissions,
    ModeratorPermissions,
    UserPermissions,
    IsAdminOrReadOnly,
    AuthorPermissions
)
from .serializers import (
    TitleSerializer,
    TitleListSerializer,
    GenreSerializer,
    CategorySerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    NotRoleChanging,
    SignUpSerializer,
    GetTokenSerializer,
)


CONFIRMATION_MESSAGE = "Ваш логин {user}, код подтверждения {token}"


class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
        )
        user.email_user(
            "Confirmation code",
            CONFIRMATION_MESSAGE.format(
                user=user.username,
                token=default_token_generator.make_token(user),
            ),
        ),
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(
            user, request.data.get["token"]
        ):
            return Response("Пользователь и код подтверждения - не совпадают")
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
            }
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminPermissions,)
    lookup_field = "username"

    @action(
        methods=["get", "patch"],
        url_path="me",
        permission_classes=(UserPermissions,),
        detail=False,
    )
    def get_self_user(self, request):
        if request.method == "PATCH":
            serializer = NotRoleChanging(
                request.user,
                data=request.data,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category__slug", "genre__slug", "name", "year")
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [AdminPermissions, ]
        return super(TitleViewSet, self).get_permissions()

    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            if (
                Title.objects.prefetch_related("reviews").order_by("name")
                is not None
            ):
                return Title.objects.all().annotate(
                    rating=Avg("reviews__score")
                )
            return Title.objects.all().set(rating=0)
        return Title.objects.all()

    # @action(detail=False, methods=["get", "post", "delete", "patch"])
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
    permission_classes = (IsAdminOrReadOnly,)


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
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    """Настройка отображения по модели Review"""

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        elif self.request.method == 'DELETE':
            self.permission_classes = [ModeratorPermissions, ]
        else:
            self.permission_classes = [AuthorPermissions, ]
        return super(ReviewViewSet, self).get_permissions()

    serializer_class = ReviewSerializer
    # permission_classes = (AuthorPermissions,)
    pagination_class = LimitOffsetPagination

    def get_title(self):
        """Получаем произведения."""
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Настройка отображения по модели Comment"""

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        elif self.request.method == 'DELETE':
            self.permission_classes = [ModeratorPermissions, ]
        else:
            self.permission_classes = [AuthorPermissions, ]
        return super(CommentViewSet, self).get_permissions()

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [AuthorPermissions, ]

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

    # def perform_update(self, serializer):
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
