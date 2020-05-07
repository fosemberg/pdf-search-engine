from django.core.management.base import BaseCommand, CommandError
from engine.models import Page, Document, ElasticPage


class Command(BaseCommand):
    help = 'populates db with test data'

    def handle(self, *args, **options):
        urls = [
            'https://storage.yandexcloud.net/pdf-storage/NUP4114_page_0.pdf',
            'https://storage.yandexcloud.net/pdf-storage/NUP4114_page_1.pdf',
            'https://storage.yandexcloud.net/pdf-storage/NUP4114_page_2.pdf',
            'https://storage.yandexcloud.net/pdf-storage/NUP4114_page_3.pdf',
            'https://storage.yandexcloud.net/pdf-storage/NUP4114_page_4.pdf',
            'https://storage.yandexcloud.net/pdf-storage/NUP4114_page_5.pdf',
            'https://storage.yandexcloud.net/pdf-storage/NUP4114_page_6.pdf'
        ]
        pages = []
        elasticPages = []

        d = Document(name='NUP4114', url='https://storage.yandexcloud.net/pdf-storage/NUP4114.pdf')
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
                text=text))

        d.pages = pages
        d.save()
        for page in elasticPages:
            page.save()

        ### DOC2
        urls = [
            'https://storage.yandexcloud.net/pdf-storage/Apem_06172019_Q14_Series-1605261-0.pdf',
            'https://storage.yandexcloud.net/pdf-storage/Apem_06172019_Q14_Series-1605261-1.pdf',
            'https://storage.yandexcloud.net/pdf-storage/Apem_06172019_Q14_Series-1605261-2.pdf',
            'https://storage.yandexcloud.net/pdf-storage/Apem_06172019_Q14_Series-1605261-3.pdf',
            'https://storage.yandexcloud.net/pdf-storage/Apem_06172019_Q14_Series-1605261-4.pdf',
            'https://storage.yandexcloud.net/pdf-storage/Apem_06172019_Q14_Series-1605261-5.pdf',
            'https://storage.yandexcloud.net/pdf-storage/Apem_06172019_Q14_Series-1605261-6.pdf',
            'https://storage.yandexcloud.net/pdf-storage/Apem_06172019_Q14_Series-1605261-7.pdf'
        ]

        pages = []
        elasticPages = []

        d = Document(name='Apem_06172019_Q14', url='https://storage.yandexcloud.net/pdf-storage/Apem_06172019_Q14_Series-1605261.pdf')
        for i in range(8):
            text = ''
            with open(f'./engine/management/commands/resourses/Apem_06172019_Q14_Series-1605261/Apem_06172019_Q14_Series-1605261-{i}-text.txt') as f:
                text = f.readline()
            
            vision = ''
            with open(f'./engine/management/commands/resourses/Apem_06172019_Q14_Series-1605261/Apem_06172019_Q14_Series-1605261-{i}-response.json') as f:
                vision = f.readline()
            
            pages.append(Page(
                url=urls[i],
                num=i+1,
                text=text,
                vision=vision,
                tables=[]))

            elasticPages.append(ElasticPage(
                name=f'Apem_06172019_Q14-{i+1}', 
                url=urls[i], num=i+1, 
                doc_name='Apem_06172019_Q14', 
                document=d, 
                text=text))

        d.pages = pages
        d.save()
        for page in elasticPages:
            page.save()

        ### DOC3
        urls = [
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-0.pdf',
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-1.pdf',
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-2.pdf',
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-3.pdf',
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-4.pdf',
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-5.pdf',
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-6.pdf',
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-7.pdf',
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-8.pdf',
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-9.pdf',
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-10.pdf',
            'https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402-11.pdf',
        ]
        pages = []
        elasticPages = []

        d = Document(name='D_3120-N_ENG', url='https://storage.yandexcloud.net/pdf-storage/D_3120-N_ENG-1525402.pdf')
        for i in range(12):
            text = ''
            with open(f'./engine/management/commands/resourses/D_3120-N_ENG-1525402/D_3120-N_ENG-1525402-{i}-text.txt') as f:
                text = f.readline()
            
            vision = ''
            with open(f'./engine/management/commands/resourses/D_3120-N_ENG-1525402/D_3120-N_ENG-1525402-{i}-response.json') as f:
                vision = f.readline()
            
            pages.append(Page(
                url=urls[i],
                num=i+1,
                text=text,
                vision=vision,
                tables=[]))

            elasticPages.append(ElasticPage(
                name=f'D_3120-N_ENG-{i+1}', 
                url=urls[i], num=i+1, 
                doc_name='D_3120-N_ENG', 
                document=d, 
                text=text))

        d.pages = pages
        d.save()
        for page in elasticPages:
            page.save()

        ### DOC4
        urls = [
            'https://storage.yandexcloud.net/pdf-storage/ile-1553267814-1588925-0.pdf',
            'https://storage.yandexcloud.net/pdf-storage/ile-1553267814-1588925-1.pdf'
        ]
        pages = []
        elasticPages = []

        d = Document(name='ile-1553267814', url='https://storage.yandexcloud.net/pdf-storage/ile-1553267814-1588925.pdf')
        for i in range(2):
            text = ''
            with open(f'./engine/management/commands/resourses/ile-1553267814-1588925/ile-1553267814-1588925-{i}-text.txt') as f:
                text = f.readline()
            
            vision = ''
            with open(f'./engine/management/commands/resourses/ile-1553267814-1588925/ile-1553267814-1588925-{i}-response.json') as f:
                vision = f.readline()
            
            pages.append(Page(
                url=urls[i],
                num=i+1,
                text=text,
                vision=vision,
                tables=[]))

            elasticPages.append(ElasticPage(
                name=f'ile-1553267814-{i+1}', 
                url=urls[i], num=i+1, 
                doc_name='ile-1553267814', 
                document=d, 
                text=text))

        d.pages = pages
        d.save()
        for page in elasticPages:
            page.save()
        
        ### DOC5
        urls = [
            'https://storage.yandexcloud.net/pdf-storage/steval-spin3204-1602123-0.pdf',
            'https://storage.yandexcloud.net/pdf-storage/steval-spin3204-1602123-1.pdf',
            'https://storage.yandexcloud.net/pdf-storage/steval-spin3204-1602123-2.pdf',
            'https://storage.yandexcloud.net/pdf-storage/steval-spin3204-1602123-3.pdf',
            'https://storage.yandexcloud.net/pdf-storage/steval-spin3204-1602123-4.pdf',
            'https://storage.yandexcloud.net/pdf-storage/steval-spin3204-1602123-5.pdf',
            'https://storage.yandexcloud.net/pdf-storage/steval-spin3204-1602123-6.pdf',
            'https://storage.yandexcloud.net/pdf-storage/steval-spin3204-1602123-7.pdf',
            'https://storage.yandexcloud.net/pdf-storage/steval-spin3204-1602123-8.pdf'            
        ]
        pages = []
        elasticPages = []

        d = Document(name='steval-spin3204', url='https://storage.yandexcloud.net/pdf-storage/steval-spin3204-1602123.pdf')
        for i in range(9):
            text = ''
            with open(f'./engine/management/commands/resourses/steval-spin3204-1602123/steval-spin3204-1602123-{i}-text.txt') as f:
                text = f.readline()
            
            vision = ''
            with open(f'./engine/management/commands/resourses/steval-spin3204-1602123/steval-spin3204-1602123-{i}-response.json') as f:
                vision = f.readline()
            
            pages.append(Page(
                url=urls[i],
                num=i+1,
                text=text,
                vision=vision,
                tables=[]))

            elasticPages.append(ElasticPage(
                name=f'steval-spin3204-{i+1}', 
                url=urls[i], num=i+1, 
                doc_name='steval-spin3204', 
                document=d, 
                text=text))

        d.pages = pages
        d.save()
        for page in elasticPages:
            page.save()
