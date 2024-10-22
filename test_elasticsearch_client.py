from elasticsearch import Elasticsearch, helpers
from elasticsearch_query import ElasticsearchClient

es_client = ElasticsearchClient()
es_client.create_index()
print("Index created successfully.")
