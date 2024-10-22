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
conda create -n rag_application python=3.9
conda activate rag_application
pip install -r requirements_version.txt
```

```cmd
docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.15.1
```

```cmd
python -m streamlit run app.py
```

