import datetime as dt

from rest_framework import serializers

from reviews.models import Categories, Genres, Titles, GenreTitle


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Genres


def validate_year(value):
    if value > dt.datetime.now().year:
        raise serializers.ValidationError('Год выпуска не может быть больше текущего')
    return value


class TitlesGetSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    year = serializers.IntegerField(validators=[validate_year])
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Titles


class TitlesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    year = serializers.IntegerField(validators=[validate_year])
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Categories.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Titles

