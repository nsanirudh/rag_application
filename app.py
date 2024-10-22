import streamlit as st
from document_loader import load_document
from elasticsearch_query import ElasticsearchClient
from config import Config
from langchain.llms import OpenAI
import os

def main():
    st.title("RAG Application with Elasticsearch")

    # Initialize Elasticsearch client
    es_client = ElasticsearchClient()

    # File upload
    uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=['pdf', 'docx', 'doc'])
    if uploaded_file is not None:
        # Save uploaded file
        file_path = os.path.join("temp_files", uploaded_file.name)
        os.makedirs("temp_files", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load and index document
        # Load and index the document
        documents = load_document(file_path)
        if documents:
            es_client.index_documents(documents)
            st.success("Document indexed successfully.")
        else:
            st.warning("No documents were loaded. Please check the file and try again.")

    # Question input
    query = st.text_input("Enter your query:")
    if query:
        retrieved_docs = es_client.search(query)
        # Display results
        for doc in retrieved_docs:
            st.write(f"Score: {doc['score']}")
            st.write(f"Text: {doc['text']}")
            st.write("---")

    if st.button("Get Answer"):
        if not query:
            st.warning("Please enter a question.")
        else:
            # Search for relevant documents
            retrieved_docs = es_client.search(query)
            if not retrieved_docs:
                st.warning("No relevant documents found.")
                return

            # Combine retrieved texts
            context = ' '.join([doc['text'] for doc in retrieved_docs])

            # Generate answer using LLM
            llm = OpenAI(openai_api_key=Config.OPENAI_API_KEY)
            prompt = f"Answer the question based on the context below:\n\nContext: {context}\n\nQuestion: {query}\nAnswer:"
            response = llm(prompt)
            st.subheader("Answer:")
            st.write(response)

if __name__ == "__main__":
    main()
