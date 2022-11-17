from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet
# UserActionsViewSet

app_name = "reviews"

router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("v1/", include(router_v1.urls))
]
