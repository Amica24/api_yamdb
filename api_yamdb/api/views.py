from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Avg
from rest_framework.exceptions import MethodNotAllowed

from reviews.models import Categories, Genres, Titles, User, Comment, Review
from .permissions import (
    IsAdmin, IsAdminOrReadOnly, ReviewComment
)
from .serializers import (
    CategoriesSerializer, GenresSerializer, SignupSerializer,
    TitlesGetSerializer, TitlesSerializer, TokenSerializer,
    UserSerializer, CommentSerializer, ReviewSerializer,
)


code_test = PasswordResetTokenGenerator()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=('GET', 'PATCH'))
    def user_func(self, request):
        user = get_object_or_404(User, username=request.user.username)

        if request.method != 'PATCH':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(
            user,
            context={'request': request},
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if self.request.user.is_superuser:
            serializer.save()
        else:
            serializer.save(role=user.role)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class SingupViewSet(viewsets.ModelViewSet):
    querryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email').lower()
        try:
            user = User.objects.get(
                username=username,
                email=email)
        except User.DoesNotExist:
            if User.objects.filter(username=username).exists():
                return Response(
                    'Username уже существует',
                    status=status.HTTP_400_BAD_REQUEST
                )
            if User.objects.filter(email=email).exists():
                return Response(
                    'Emial уже существует',
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = User.objects.create_user(username=username, email=email)
        user.is_active = False
        user.save()
        confirmation_code = (
            PasswordResetTokenGenerator().make_token(user)
        )
        message = f'Код подтверждения - {confirmation_code}'
        send_mail(
            'Ваш код подтверждения',
            message,
            'api_yambd@example.com',
            (email, )
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class TokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if not code_test.check_token(user, confirmation_code):
            return Response(
                {'confirmation_code': ['Код не действителен!']},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(ListCreateDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializer
        else:
            return TitlesSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewComment,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        return Comment.objects.filter(review_id=review.id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review_id=review.id)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewComment,)
 #   http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        return Review.objects.filter(title_id=title.id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(author=self.request.user, title_id=title.id)

#    def create(self, request, *args, **kwargs):
#        if self.request.method == 'PUT':
#            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#        serializer = self.get_serializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        self.perform_create(serializer)
#        headers = self.get_success_headers(serializer.data)
# #       if serializer.context.get('request').method == 'PUT':
# #           return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
    def update(self, request, *args, **kwargs):
   #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if request.method == 'PUT':
            raise MethodNotAllowed(method='PUT')
        return super().update(request, *args, **kwargs)
   #     if request.method == 'PUT':
   #         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
 #       partial = kwargs.pop('partial', False)
 #       instance = self.get_object()
 #       serializer = self.get_serializer(instance, data=request.data, partial=partial)
 #       serializer.is_valid(raise_exception=True)
 #       self.perform_update(serializer)
#
 #       if getattr(instance, '_prefetched_objects_cache', None):
 #           # If 'prefetch_related' has been applied to a queryset, we need to
 #           # forcibly invalidate the prefetch cache on the instance.
 #           instance._prefetched_objects_cache = {}
 #       
 # #      if serializer.context.get('request').method == 'PUT':
 # #          return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
 #       return Response(serializer.data)
