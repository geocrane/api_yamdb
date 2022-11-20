from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from reviews.models import User

from .serializers import SignUpSerializer, GetTokenSerializer

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
