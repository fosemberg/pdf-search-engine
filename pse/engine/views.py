import os
import uuid
import logging

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser

from .models import Document, Page, ElasticPage
from .utils import pdf_parser, search_utils, table_utils, storage_upload, image_utils

logger = logging.getLogger(__name__)

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
        logger.info('advanced search')
        responce = search_utils.elastic_search(name, query)
    else: 
        logger.info('regular search')
        responce = search_utils.slow_search(name, query)
    logger.info('search responce', responce)

    return JsonResponse(responce, status=status.HTTP_200_OK)

@csrf_exempt
def upload(request):
    if request.method != 'POST':
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    pdf_file = request.FILES['file']
    document_name = request.POST['filename']

    # TODO delete tmp files
    logger.info(f'savig tmp file to disk')
    pdf_tmp_file_name = f'/tmp/{uuid.uuid4()}.tmp'
    with open(pdf_tmp_file_name, 'wb+') as destination:
        for chunk in pdf_file.chunks():
            destination.write(chunk)

    logger.info(f'getting images from file')
    with open(pdf_tmp_file_name, 'rb') as f:
        images = image_utils.extract_images(f)

    logger.info(f'saving whole file to s3')
    with open(pdf_tmp_file_name, 'rb') as f:
        document_url = storage_upload.fileobj2url(f, f'{document_name}.pdf')
        if document_url['error'] is not None:
            return HttpResponse('Unable to load the file', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    logger.info('saving pages to tmp files')
    tmp_page_names = []
    with open(pdf_tmp_file_name, 'rb') as f:
        pdf_pages = pdf_parser.split_file_to_pages(f)
        logger.info(f'found {len(pdf_pages)} pages')
        for p in pdf_pages:
            tmp_page_names.append(f'/tmp/{uuid.uuid4()}.tmp')
            with open(tmp_page_names[-1], 'wb+') as pf:
                pf.write(p.read()) 

    logger.info('saving pages to s3')
    page_urls = []
    for i in range(len(tmp_page_names)):
        logger.info(f'processing page {i}/{len(tmp_page_names)}')
        with open(tmp_page_names[i], 'rb') as pf:
            logger.info(f'uploading page to s3')
            page_url = storage_upload.fileobj2url(pf, f'{document_name}_page_{i}.pdf')
            if page_url['error'] is not None:
                return HttpResponse('Unable to load the file', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            page_urls.append(page_url['url'])
            
    logger.info('saving yandex vision response to mongo and elastic')
    document = Document(name=document_name, url=document_url['url'])
    pages = []
    elastic_pages = []
    for i in range(len(tmp_page_names)):
        logger.info(f'processing page {i}/{len(tmp_page_names)}')
        with open(tmp_page_names[i], 'rb') as pf:
            logger.info('uploading page to yandex vision')
            vision, text = pdf_parser.parse_pdf(pf)
        with open(tmp_page_names[i], 'rb') as pf:
            # TODO need to save in format: 'doc_name-page_num-table-num'
            tables = table_utils.save_tables_from_page(pf, i)
        tables = []
        pages.append(
            Page(url=page_urls[i], num=i+1, text=text, vision=vision, tables=tables, images=images[i])
        )
        elastic_pages.append(
            ElasticPage(url=page_urls[i], num=i+1, text=text, document=document, name=f'document_name-{i+1}', doc_name=document_name)
        )

    # TODO simplify after splitting models
    document.pages = pages
    print(f'saving pages {pages}')
    document.save()
    print(f'saving elastic-pages {elastic_pages}')
    for page in elastic_pages:
        print(f'saving elastic-page {page}')
        page.save()

    return HttpResponse(status=status.HTTP_201_CREATED)

