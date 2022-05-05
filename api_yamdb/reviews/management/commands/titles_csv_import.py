import os

from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Titles, Categories


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Titles.objects.exists():
            print('Titles data already loaded...exiting.')
            return

        print('Loading Titles data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'titles.csv'
        )
        for row in DictReader(open(path)):
            title = Titles(
                pk=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )
            title.save()
