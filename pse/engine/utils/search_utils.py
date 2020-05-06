import re
from elasticsearch.exceptions import RequestError

from engine.models import Document, Page
from engine.documents import PageDocument

def elastic_search(doc_name, query):
    try: 
        document = Document.objects.filter(name=doc_name).first()
        res = {doc_name: {}}
        query_string = f'doc_name:"{doc_name}" AND text:({query})'
        print(f'elastic search query string <{query_string}>')
        for page in PageDocument.search().query('query_string', query=query_string): 
            if page.doc_name not in res:
                res[page.doc_name] = {}
            res[doc_name][page.num] = {
                'url': page.url,
                'tables': {},
                'images': {},
            }

        for page_num in res[doc_name]:
            page = document.pages[page_num-1]
            for t in page.tables:
                res[doc_name][page_num]['tables'][t.num] = t.url
            for im in page.images:
                res[doc_name][page_num]['images'][im.num] = im.url

        return res
    except RequestError as e:
        print(e)
        return {"error": True, "text": "invalid query syntax"}


def slow_search(doc_name, query):
    try:
        keywords = query.split()
        patterns = [re.compile(r'\b{}\b'.format(word), re.IGNORECASE) for word in keywords]
        documents = Document.objects.filter(name=doc_name)
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
        return results
    except Exception as e:
        print(e)
