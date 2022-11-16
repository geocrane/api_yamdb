from django.urls import path

from .views import GetTokenAPIView, SignUpAPIView

app_name = "authentication"

urlpatterns = [
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
