import re
from elasticsearch.exceptions import RequestError

from engine.models import Document, Page
from engine.documents import PageDocument

def elastic_search(doc_name, query):
    try: 
        res = {doc_name: {}}
        for page in PageDocument.search().query('query_string', query=f'doc_name:"{doc_name}" AND text:({query})'): 
            if page.doc_name not in res:
                res[page.doc_name] = {}
            res[doc_name][page.num] = page.url
        return res
    except RequestError as e:
        print(e)
        return {"error": True, "text": "invalid query syntax"}


def slow_search(query):
    keywords = query.split() 
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
    return results