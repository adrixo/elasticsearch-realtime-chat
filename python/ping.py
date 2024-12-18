from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

USERNAME = "elastic"
PASSWORD = "changeme"

es = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False  # Allow self-signed certificates
)

try:
    if es.ping():
        print("Successfully connected to Elasticsearch with authentication!")
    else:
        print("Connection failed.")
except ConnectionError:
    print("Unable to connect to Elasticsearch.")
