from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from engine.models import Document, Page
from rest_framework import status
from rest_framework.parsers import JSONParser

import re

from pse.utils import pdf_parser
from utils import storage_upload
from pse.utils import table_utils
from pse.utils import image_utils


@csrf_exempt
def get_all(request):
    if request.method == 'GET':
        component_names_query_set = Document.objects.all().values_list('name', flat=True)

        result = dict()
        result['names'] = list(component_names_query_set)

        return JsonResponse(result, status=status.HTTP_200_OK)


@csrf_exempt
def fast_search(request):
    # TODO: fix this regex matching
    if request.method == 'POST':
        data = JSONParser().parse(request)
        name = data['name']
        keywords = data['keywords'].split()
        ods = [i for i in Document.objects.mongo_aggregate([
            {'$match': {'name': name}},
            {'$project': {
                'pages': {
                    '$filter': {
                        'input': '$pages',
                        'as': 'page',
                        'cond': {
                            '$and': [{'$regexMatch':
                                         {'input': '$$page.text', 'regex': '/.*{}.*/'.format(key), 'options': 'i'}
                                     } for key in keywords
                                    ]
                         }
                    }
                }
            }},
            {'$unset': ['pages.vision']}
        ])]

        # conversion to json format
        print(ods)
        results = dict()
        for od in ods:
            pages = dict(od)['pages']
            found_in_document = dict()
            for p in pages:
                p = dict(p)
                found_in_document[p['num']] = p['url']
            results[name] = found_in_document

        return JsonResponse(results, status=status.HTTP_200_OK)


@csrf_exempt
def slow_search(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        name = data['name']
        keywords = data['keywords'].split()
        patterns = [re.compile(r'\b{}\b'.format(word), re.IGNORECASE) for word in keywords]
        documents = Document.objects.filter(name=name)

        results = dict()
        for document in documents:
            found_in_document = dict()
            pages = document.pages
            for page in pages:
                has_all_words = all(p.search(page.text) for p in patterns)
                if has_all_words:

                    found_in_document[page.num] = dict()
                    found_in_document[page.num]['url'] = page.url
                    found_in_document[page.num]['tables'] = dict()
                    found_in_document[page.num]['images'] = dict()
                    for t in page.tables:
                        found_in_document[page.num]['tables'][t.num] = t.url
                    for im in page.images:
                        found_in_document[page.num]['images'][im.num] = im.url

            results[document.name] = found_in_document
        return JsonResponse(results, status=status.HTTP_200_OK)


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        pdf_file = request.FILES['file']
        document_name = request.POST['filename']
        images = image_utils.extract_images(pdf_file)
        pdf_pages = pdf_parser.split_file_to_pages(pdf_file)
        pages = []
        for i in range(len(pdf_pages)):
            vision, text = pdf_parser.parse_pdf(pdf_pages[i])
            # line below closes page
            tables = table_utils.save_tables_from_page(pdf_pages[i], i)
            url = storage_upload.fileobj2url(pdf_pages[i], '{}_page_{}'.format(document_name, i))
            if url['error'] is not None:
                return HttpResponse('Unable to load the file', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            pages.append(
                Page(
                    url=url['url'],
                    num=i + 1,
                    text=text,
                    vision=vision,
                    tables=tables,
                    images=images[i]
                )
            )

        # saving document to storage
        document_url = storage_upload.fileobj2url(pdf_file, document_name)
        if document_url['error'] is not None:
            return HttpResponse('Unable to load the file', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # saving document
        d = Document(name=document_name, url=document_url, pages=pages)
        d.save()
        return HttpResponse(status=status.HTTP_201_CREATED)

    return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
