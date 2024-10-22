from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import ElasticVectorSearch
from config import Config

class EmbeddingStore:
    def __init__(self):
        self.es = Elasticsearch(
            Config.ELASTICSEARCH_HOST,
            http_auth=(Config.ELASTICSEARCH_USERNAME, Config.ELASTICSEARCH_PASSWORD),
            verify_certs=False  # For development only
        )
        self.embedding = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.index_name = Config.INDEX_NAME

    def index_documents(self, documents):
        vector_store = ElasticVectorSearch(
            elasticsearch_url=Config.ELASTICSEARCH_HOST,
            index_name=self.index_name,
            embedding=self.embedding,
        )
        vector_store.add_documents(documents)
