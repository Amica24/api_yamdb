from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (
#     # TokenObtainPairView,
#     TokenRefreshView,
# )

from .views import SingupViewSet, TokenViewSet

router = DefaultRouter()
router.register(
    'auth/token', TokenViewSet, basename='Token'
)
router.register(
    'auth/signup', SingupViewSet, basename='signup'
)


urlpatterns = [
    path('', include(router.urls)),
]
