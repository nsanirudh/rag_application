from config import Config
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from retriever import Retriever

class RAGChain:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=Config.OPENAI_API_KEY
        )
        # self.llm = OpenAI(openai_api_key=Config.OPENAI_API_KEY)

    def generate_answer(self, query):
        retrieved_docs = self.retriever.retrieve(query)
        context = ' '.join([doc.page_content for doc in retrieved_docs])
        prompt = f"Answer the question based on the context below:\n\nContext: {context}\n\nQuestion: {query}\nAnswer:"
        response = self.llm(prompt)
        return response
