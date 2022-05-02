import os

from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Categories


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Categories.objects.exists():
            print('Categories data already loaded...exiting.')
            return

        print('Loading Categories data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'category.csv'
        )
        for row in DictReader(open(path)):
            category = Categories(
                pk=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            category.save()
