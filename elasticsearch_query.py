from elasticsearch import Elasticsearch, helpers
from langchain_openai import OpenAIEmbeddings
from config import Config
import numpy as np
import json
import numpy as np
import os
import joblib



class ElasticsearchClient:
    def __init__(self):
        self.es = Elasticsearch(
            Config.ELASTICSEARCH_HOST,
            http_auth=(Config.ELASTICSEARCH_USERNAME, Config.ELASTICSEARCH_PASSWORD),
        )
        self.index_name = Config.INDEX_NAME
        self.embedding_dim = 1536  # Replace with your embedding dimension

    def create_index(self):
        # Delete the existing index if it exists
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)
            print(f"Deleted existing index '{self.index_name}'.")

        # Define index mapping with dense_vector and index enabled
        mapping = {
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "metadata": {
                        "properties": {
                            "source": {"type": "text"},
                            "page": {"type": "integer"}
                        }
                    },
                    "embedding": {
                        "type": "dense_vector",
                        "dims": self.embedding_dim,  # Should be 1536
                        "index": True,
                        "similarity": "cosine"  # Use 'l2_norm' or 'dot_product' if preferred
                    }
                }
            }
        }

        # Create the index
        self.es.indices.create(index=self.index_name, body=mapping)
        print(f"Created index '{self.index_name}' with embedding dimension {self.embedding_dim}.")

    def index_documents(self, documents):
        print("Starting indexing of documents...")

        # Generate embeddings
        embeddings_model = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        texts = [doc.page_content for doc in documents]
        embeddings = embeddings_model.embed_documents(texts)

        # Ensure embeddings are lists of floats
        embeddings = [
            embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
            for embedding in embeddings
        ]

        # Update index mapping with correct dimension
        self.create_index()

        # Index documents individually
        for i, doc in enumerate(documents):
            document = {
                "text": doc.page_content,
                "metadata": doc.metadata,
                "embedding": embeddings[i],
            }
            try:
                self.es.index(index=self.index_name, id=i, body=document)
                print(f"Document {i} indexed successfully.")
            except Exception as e:
                print(f"Failed to index document {i}: {e}")
                if hasattr(e, 'body'):
                    print(f"Error body: {e.body}")
                print(f"Document that failed: {document}")

        print("Indexing completed.")

    def search(self, query_text, top_k=5):
        # Generate embedding for the query
        embeddings_model = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        query_vector = embeddings_model.embed_query(query_text)

        num_candidates = 1000
        # Construct the search query with 'knn' at the top level
        search_query = {
            "size": top_k,
            "knn": {
                "field": "embedding",
                "query_vector": query_vector,
                "k": top_k,
                "num_candidates": num_candidates
            }
        }

        # Execute the search query
        response = self.es.search(index=self.index_name, body=search_query)

        # Parse the response
        hits = response['hits']['hits']
        results = []
        for hit in hits:
            source = hit['_source']
            doc = {
                'text': source['text'],
                'metadata': source.get('metadata', {}),
                'score': hit.get('_score', 0)
            }
            results.append(doc)
        return results





