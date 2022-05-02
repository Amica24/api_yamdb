from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet, GenresViewSet, SingupViewSet,
    TitlesViewSet, TokenViewSet, UserViewSet,
    ReviewViewSet, CommentViewSet,
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
    r'titles', TitlesViewSet
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('', include(router.urls)),
]
