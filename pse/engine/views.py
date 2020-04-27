from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from engine.models import Document, Page
from rest_framework import status
from rest_framework.parsers import JSONParser

import re


@csrf_exempt
def fast_search(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        name = data['name']
        keywords = data['keywords']
        ods = [i for i in Document.objects.mongo_aggregate([
            {'$match': {'name': name}},
            {'$project': {
                'pages': {
                    '$filter': {
                        'input': '$pages',
                        'as': 'page',
                        'cond': {
                            '$or': [{'$regexMatch':
                                         {'input': '$$page.text', 'regex': '/.*{}.*/'.format(key)}
                                     } for key in keywords
                                    ]
                         }
                    }
                }
            }},
            {'$unset': ['pages.text', 'pages.vision']}
        ])]

        # conversion to json format
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
        keywords = data['keywords']
        pattern = re.compile('|'.join(r'\b{}\b'.format(word) for word in keywords))
        documents = Document.objects.filter(name=name)
        results = dict()
        for document in documents:
            found_in_document = dict()
            pages = document.pages
            for page in pages:
                if pattern.search(page.text) is not None:
                    found_in_document[page.num] = page.url
            results[document.name] = found_in_document
        return JsonResponse(results, status=status.HTTP_200_OK)


