from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny)
from reviews.models import Comment, Review, Title, Category, Genre, User
from api.permissions import (
    AdminPermissions,
    UserPermissions,
    ModeratorPermissions,
    IsUserOrReadOnly,
    IsAuthorOrModeRatOrOrAdminOrReadOnly,)
from .serializers import (
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    NotRoleChanging,
    TitleListSerializer
)
from rest_framework.decorators import action
from .mixins import CreateDeleteViewSet
from rest_framework import status
from rest_framework import viewsets, filters


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    lookup_field = "username"

    @action(
        methods=["get", "patch"],
        url_path="me",
        permission_classes=(IsAuthenticated,),
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
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            if Title.objects.prefetch_related(
                'reviews').order_by('name') is not None:
                return Title.objects.all().annotate(
                    rating=Avg('reviews__score')
                )
            return 'rating' is None
        return Title.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleSerializer


class GenreViewSet(CreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    pagination_class = LimitOffsetPagination
    """permission_classes = (IsAdminOrReadOnly,)"""


class CategoryViewSet(CreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    pagination_class = LimitOffsetPagination
    """permission_classes = (IsAdminOrReadOnly,)"""


class ReviewViewSet(viewsets.ModelViewSet):
    """Настройка отображения по модели Review"""

    serializer_class = ReviewSerializer
    permission_classes = (
        # IsUserOrReadOnly,
        # AdminPermissions,
        # UserPermissions,
        # ModeratorPermissions,
    )
    pagination_class = PageNumberPagination

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

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsUserOrReadOnly,
        AdminPermissions,
        UserPermissions,
        ModeratorPermissions,

    )

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

    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
