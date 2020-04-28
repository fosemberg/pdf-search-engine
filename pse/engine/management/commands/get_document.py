from django.core.management.base import BaseCommand, CommandError
from engine.models import Page, Document


class Command(BaseCommand):
    help = 'populates db with test data'

    def add_arguments(self, parser):
        parser.add_argument('--name', default='NUP4114')

    def handle(self, *args, **options):
        d = Document.objects.all().filter(name=options['name']).first()
        print(f'Found document: {d}')
        if not d:
            return
        for page in d.pages:
            print(page, f'text: {page.text[:50]}...')
