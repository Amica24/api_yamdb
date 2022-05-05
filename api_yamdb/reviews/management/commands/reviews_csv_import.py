import os

from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Review


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Review.objects.exists():
            print('Review data already loaded...exiting.')
            return

        print('Loading Review data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'review.csv'
        )
        for row in DictReader(open(path)):
            review = Review(
                pk=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()
