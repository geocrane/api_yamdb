from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# from .serializers import RegistrationSerializer, SignUpSerializer
from .models import User

CONFIRMATION_MESSAGE = "Ваш логин {user}, код подтверждения {token}"


class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = User.objects.create_user(
            username=request.data["username"], email=request.data["email"]
        )
        user.email_user(
            "Confirmation code",
            CONFIRMATION_MESSAGE.format(
                user=user.username,
                token=default_token_generator.make_token(user),
            ),
        ),
        return Response(status=status.HTTP_200_OK)


class GetTokenAPIView(APIView):
    def post(self, request):
        username = request.data["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not default_token_generator.check_token(
            user, request.data["token"]
        ):
            return Response("Пользователь и код подтверждения - не совпадают")
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )