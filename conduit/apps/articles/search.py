
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, DocType, Text, Date, Keyword

from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models


connections.create_connection()

class ArticleIndex(Document):

    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    description = Text()
    author = Text()
    created_at = Date()
    updated_at = Date()
    body = Text(analyzer='snowball')
    tags = Keyword()

    class Index:
        name = 'article'
        settings = {
          "number_of_shards": 2,
        }


def bulk_indexing():
    ArticleIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Article.objects.all().iterator()))
