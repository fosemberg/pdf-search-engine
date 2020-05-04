from django_elasticsearch_dsl import Document, fields

from django_elasticsearch_dsl.registries import registry
from .models import ElasticPage

@registry.register_document
class PageDocument(Document):

    class Index:
        name = 'pages'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = ElasticPage 

        fields = [
            'url',
            'num', 
            'text',
            'doc_name',
            'name'
        ]
