from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

USER = 'user'
MODERATOR = 'moder'
ADMIN = 'admin'

ROLES = [
    (USER, 'user'),
    (MODERATOR, 'moder'),
    (ADMIN, 'admin'),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='username',
        validators=[RegexValidator(r'^[\w.@+-]+')]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='mail'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='name'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='last_name'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='bio'
    )
    role = models.CharField(
        max_length=10,
        verbose_name='role',
        default=USER,
        choices=ROLES,
    )
    confirmation_code = models.CharField(
        max_length=256,
        blank=True,
        verbose_name='confirmation_code'
    )

    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
