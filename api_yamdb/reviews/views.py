from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny

from .permissions import AuthorOrReadOnly
from .serializers import UserSerializer

from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    lookup_field = "username"

    def patch(self, request):
        if self.kwargs["username"] == "me":
            pass





# class UserActionsViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny,)

#     def get_queryset(self):
#         return get_object_or_404(User, username=self.kwargs["username"])
