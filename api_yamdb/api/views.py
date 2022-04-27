from rest_framework import filters, mixins, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Categories, Genres, Titles
from .permissions import IsAdminOrReadOnly
from .serializers import CategoriesSerializer, GenresSerializer, TitlesSerializer


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class GenresViewSet(ListCreateDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
