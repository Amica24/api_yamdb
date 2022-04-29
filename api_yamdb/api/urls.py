from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SingupViewSet, TokenViewSet,
    UserViewSet
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


urlpatterns = [
    path('', include(router.urls)),
]
