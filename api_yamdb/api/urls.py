
from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from api.views import (CommentViewSet, ReviewViewSet)


router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'reviews', ReviewViewSet, basename='reviews')
#router.register(
    #r'title/(?P<title_id>\d+)/reviews', CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
]
