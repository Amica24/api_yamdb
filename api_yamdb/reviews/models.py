import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
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

    class Meta:
        ordering = ['id']

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


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг категории'
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг жанра'
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


def validate_year(value):
    if value > dt.datetime.now().year:
        raise ValidationError(
            'Год выпуска не может быть больше текущего'
        )
    return value


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        db_index=True
    )
    year = models.IntegerField(
        'Год выпуска',
        db_index=True,
        validators=[validate_year]
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        related_name='title',
        verbose_name='Категория произведения',
        on_delete=models.SET_DEFAULT,
        default='Категория не указана',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.SET_DEFAULT,
        default='Жанр не указан'
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'],
            name='unique_review',
        )]
        ordering = ['id']


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text
