import os

from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Genre.objects.exists():
            print('Genre data already loaded...exiting.')
            return

        print('Loading Genre data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'genre.csv'
        )
        for row in DictReader(open(path)):
            genre = Genre(
                pk=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            genre.save()
