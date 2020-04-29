from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from engine.models import Document, Page
from rest_framework import status
from rest_framework.parsers import JSONParser

import re


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
                    found_in_document[page.num] = page.url
            results[document.name] = found_in_document
        return JsonResponse(results, status=status.HTTP_200_OK)


