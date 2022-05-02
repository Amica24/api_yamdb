import datetime as dt

from rest_framework import serializers

from reviews.models import Categories, Genres, Titles, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        ]


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Никнейм "me" запрещен.'
            )
        return value
      

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'name',
            'slug'
        )
        lookup_field = 'slug'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
          'name',
          'slug'
        )
        lookup_field = 'slug'
        model = Genres


def validate_year(value):
    if value > dt.datetime.now().year:
        raise serializers.ValidationError(
          'Год выпуска не может быть больше текущего'
        )
    return value


class TitlesGetSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    year = serializers.IntegerField(validators=[validate_year])
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer()

    class Meta:
        fields = (
          'id',
          'name',
          'year',
          'description',
          'genre',
          'category'
        )
        model = Titles


class TitlesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    year = serializers.IntegerField(validators=[validate_year])
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        fields = (
          'id',
          'name',
          'year',
          'description',
          'genre',
          'category'
        )
        model = Titles
