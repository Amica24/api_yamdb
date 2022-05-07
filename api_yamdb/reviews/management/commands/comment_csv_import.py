import os

from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Comment


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Comment.objects.exists():
            print('Comment data already loaded...exiting.')
            return

        print('Loading Comment data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'comments.csv'
        )
        for row in DictReader(open(path)):
            comment = Comment(
                pk=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date'],
            )
            comment.save()
