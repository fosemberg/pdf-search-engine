from django.core.management.base import BaseCommand, CommandError
from engine.models import Page, Document, ElasticPage


class Command(BaseCommand):
    help = 'populates db with test data'

    def handle(self, *args, **options):
        urls = [
            'https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114-1.pdf',
            'https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114-2.pdf',
            'https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114-3.pdf',
            'https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114-4.pdf',
            'https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114-5.pdf',
            'https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114-6.pdf',
            'https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114-7.pdf'
        ]
        pages = []
        elasticPages = []

        d = Document(name='NUP4114', url='https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114.pdf')
        for i in range(7):
            text = ''
            with open(f'./engine/management/commands/resourses/NUP4114/NUP4114-{i}-text.txt') as f:
                text = f.readline()
            
            vision = ''
            with open(f'./engine/management/commands/resourses/NUP4114/NUP4114-{i}-response.json') as f:
                vision = f.readline()
            
            pages.append(Page(
                url=urls[i],
                num=i+1,
                text=text,
                vision=vision,
                tables=[]))
            
            elasticPages.append(ElasticPage(
                name=f'NUP4114-{i+1}', 
                url=urls[i], num=i+1, 
                doc_name='NUP4114', 
                document=d, 
                text=text
            ))
        d.pages = pages
        d.save()
        for page in elasticPages:
            page.save()
