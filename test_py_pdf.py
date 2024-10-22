from langchain_community.document_loaders import PyPDFLoader

def load_document(file_path):
    documents = []
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} documents.")
    except Exception as e:
        print(f"Error loading document: {e}")
    return documents


pdf = load_document("/Users/anirudh/Downloads/2409.08069v1.pdf")
print(pdf)
