from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router = DefaultRouter()


# router.register(r'auth', ViewSet) Михаил
# router.register('users/me', ViewSet) Михаил
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenresViewSet)
router.register(r'titles', TitlesViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
