from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from engine.models import Document, Page
import re

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser


@csrf_exempt
def index(request):
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
        # pages = Document.objects.filter(name=name).aggregate([
        #     {'$unwind': "$pages"}
        # ])
        return JsonResponse(results)


