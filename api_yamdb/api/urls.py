from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
  CategoriesViewSet, GenresViewSet, SingupViewSet,
  TitlesViewSet, TokenViewSet, UserViewSet
)

router = DefaultRouter()


router.register(
    'auth/token', TokenViewSet, basename='Token'
)
router.register(
    'auth/signup', SingupViewSet, basename='signup'
)
router.register(
    'users', UserViewSet, basename='user_view'
)
router.register(
  r'categories', CategoriesViewSet
)
router.register(
  r'genres', GenresViewSet
)
router.register(
  r'titles', TitlesViewSet, basename='titles'
)

urlpatterns = [
    path('', include(router.urls)),
]
