from config import Config
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from elasticsearch_query import ElasticsearchClient

class RAGChain:
    def __init__(self):
        self.es_client = ElasticsearchClient()
        self.llm = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=Config.OPENAI_API_KEY
        )

    def generate_answer(self, query):
        retrieved_docs = self.es_client.search(query)
        if not retrieved_docs:
            st.warning("No relevant documents found.")
            return
        context = ' '.join([doc["text"] for doc in retrieved_docs])
        print(context)
        prompt = f"Answer the question based on the context below:\n\nContext: {context}\n\nQuestion: {query}\nAnswer:"
        response = self.llm(prompt)
        return response
