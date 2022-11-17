from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

v1_router = routers.DefaultRouter()
v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
