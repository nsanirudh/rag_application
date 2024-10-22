import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')
    ELASTICSEARCH_PORT = int(os.getenv('ELASTICSEARCH_PORT', '9200'))
    INDEX_NAME = os.getenv('INDEX_NAME', 'documents')
    ELASTICSEARCH_USERNAME = os.getenv('ELASTICSEARCH_USERNAME', 'elastic')
    ELASTICSEARCH_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD')
    INDEX_NAME = os.getenv('INDEX_NAME', 'documents')
    USE_SSL = os.getenv('USE_SSL', 'False') == 'True'  # Adjust based on your setup
