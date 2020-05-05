import os

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser

from .models import Document, Page, ElasticPage
from .utils import pdf_parser, search_utils, table_utils, storage_upload

@csrf_exempt
def get_all(request):
    if request.method != 'GET':
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    component_names_query_set = Document.objects.all().values_list('name', flat=True)
    result = {'names': list(component_names_query_set)}
    return JsonResponse(result, status=status.HTTP_200_OK)


@csrf_exempt
def search(request):
    if request.method != 'POST':
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    print(request)

    data = JSONParser().parse(request)
    name = data['name']
    query = data['keywords']

    if data.get('advanced'):
        print('advanced search')
        responce = search_utils.elastic_search(name, query)
    else: 
        print('regular search')
        responce = search_utils.slow_search(name, query)
    print('search responce', responce)

    return JsonResponse(responce, status=status.HTTP_200_OK)

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        pdf_file = request.FILES['file']
        document_name = request.POST['filename']
        pdf_pages = pdf_parser.split_file_to_pages(pdf_file)
        document = Document(name=document_name, url="")
        pages = []
        elastic_pages = []
        for i in range(len(pdf_pages)):
            vision, text = pdf_parser.parse_pdf(pdf_pages[i])
            # line below closes page
            tables = table_utils.save_tables_from_page(pdf_pages[i], i)
            url = storage_upload.fileobj2url(pdf_pages[i], '{}_page_{}.pdf'.format(document_name, i))
            if url['error'] is not None:
                return HttpResponse('Unable to load the file', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            pages.append(
                Page(
                    url=url['url'],
                    num=i + 1,
                    text=text,
                    vision=vision,
                    tables=tables
                )
            )
            elastic_pages.append(
                ElasticPage(
                    url=url['url'],
                    num=i+1,
                    text=text,
                    document=document,
                    name=f'document_name-{i+1}',
                    doc_name=document_name
                )
            )

        # saving document to storage
        document_url = storage_upload.fileobj2url(pdf_file, document_name)
        if document_url['error'] is not None:
            return HttpResponse('Unable to load the file', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # saving document to mongodb and elastic search
        document.pages = pages
        document.url = document_url
        print(f'saving pages {pages}')
        document.save()
        print(f'saving elastic-pages {elastic_pages}')
        for page in elastic_pages:
            print(f'saving elastic-page {page}')
            page.save()
        return HttpResponse(status=status.HTTP_201_CREATED)

    return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
