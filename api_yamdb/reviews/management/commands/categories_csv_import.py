import os

from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Category.objects.exists():
            print('Category data already loaded...exiting.')
            return

        print('Loading Category data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'category.csv'
        )
        for row in DictReader(open(path)):
            category = Category(
                pk=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            category.save()
