from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch
from langchain_openai import OpenAIEmbeddings
from config import Config

class Retriever:
    def __init__(self):
        self.embedding = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.vector_store = ElasticVectorSearch(
            elasticsearch_url=Config.ELASTICSEARCH_HOST,
            index_name=Config.INDEX_NAME,
            embedding=self.embedding
        )

    def retrieve(self, query, top_k=5):
        retriever = self.vector_store.as_retriever(search_kwargs={"k": top_k})
        return retriever.invoke(query)
