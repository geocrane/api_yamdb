from rest_framework import status

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

# from .serializers import RegistrationSerializer, SignUpSerializer
from .models import User


class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = User.objects.create_user(
            username=request.data["username"], email=request.data["email"]
        )
        token = default_token_generator.make_token(user)
        send_mail(
            "Confirmation_code",
            token,
            "from@yamdb.ru",
            [user.email],
            fail_silently=False,
        )
        return Response(status=status.HTTP_201_CREATED)


class GetTokenAPIView(APIView):
    def post(self, request):
        user = User.objects.get(username=request.data["username"])
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
