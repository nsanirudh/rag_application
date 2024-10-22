* Langchain
* OpenAI
* Elasticsearch
* Elasticsearch-dsl
* PyPDF2
* python-docx
* nltk
* streamlit
* python-dotenv
* Docker

Docker used in security disabled manner


```cmd
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.15.1
```

```cmd
conda activate rag_application
```

```cmd
docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.15.1
```

```cmd
python -m streamlit run app.py
```

