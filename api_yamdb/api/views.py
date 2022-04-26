from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from .serializers import (
    SignupSerializer,
    TokenSerializer,
)


class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user, is_created = User.objects.get_or_create(
            email=email,
            username=username
        )
        confirmation_code = (
            PasswordResetTokenGenerator().make_token(user)
        )
        message = f'Код подтверждения - {confirmation_code}'

        if is_created:
            user.is_active = False
            user.save()

        send_mail(
            'Ваш код подтверждения',
            message,
            'api_yambd@example.com',
            (email, )
        )

        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK
        )


class TokenView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)

        if PasswordResetTokenGenerator().check_token(user, confirmation_code):
            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)

        return Response(
            {'confirmation_code': ['Код не действителен!']},
            status=status.HTTP_400_BAD_REQUEST
        )
