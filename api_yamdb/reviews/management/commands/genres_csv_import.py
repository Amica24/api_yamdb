import os

from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Genres


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Genres.objects.exists():
            print('Genres data already loaded...exiting.')
            return

        print('Loading Genres data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'genre.csv'
        )
        for row in DictReader(open(path)):
            genre = Genres(
                pk=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            genre.save()
