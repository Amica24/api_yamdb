from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    genre = models.ForeignKey(
        Genres,
        related_name='title',
        on_delete=models.SET_DEFAULT,
        default='Жанр не указан',
    )
    category = models.ForeignKey(
        Categories,
        related_name='title',
        on_delete=models.SET_DEFAULT,
        default='Категория не указана',
    )

    def __str__(self):
        return self.name
