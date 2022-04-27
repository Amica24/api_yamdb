import datetime as dt

from rest_framework import serializers

from reviews.models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genres


def validate_year(value):
    if value > dt.datetime.now().year:
        raise serializers.ValidationError('Год выпуска не может быть больше текущего')
    return value


class TitlesSerializer(serializers.ModelSerializer):
    description = serializers.StringRelatedField(required=False)
    year = serializers.IntegerField(validators=[validate_year])
    genre = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Categories.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Titles
