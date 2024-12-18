from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError

USERNAME = "elastic"
PASSWORD = "changeme"

es = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)
try:
    if es.ping():
        print("Successfully connected to Elasticsearch!")
    else:
        print("Connection failed.")
except ConnectionError:
    print("Unable to connect to Elasticsearch.")

# Step 2: Create an Index (Elasticsearch equivalent to "database")
INDEX_NAME = "my_first_index"

# Define the index mapping (schema)
index_mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "age": {"type": "integer"},
            "city": {"type": "text"},
            "description": {"type": "text"}
        }
    }
}

# Check if index exists, create it if not
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body=index_mapping)
    print(f"Index '{INDEX_NAME}' created!")
else:
    print(f"Index '{INDEX_NAME}' already exists.")

# Step 3: Insert Data into Elasticsearch
documents = [
    {"name": "John Doe", "age": 28, "city": "New York", "description": "Software engineer"},
    {"name": "Jane Smith", "age": 34, "city": "San Francisco", "description": "Data scientist"},
    {"name": "Sam Brown", "age": 25, "city": "Los Angeles", "description": "UX Designer"}
]

# Insert documents
for i, doc in enumerate(documents):
    es.index(index=INDEX_NAME, id=i+1, document=doc)
print("Documents inserted successfully!")

# Step 4: Search for Data Using Patterns
# Example: Find all documents with "engineer" in the description
query = {
    "query": {
        "match": {
            "description": "engineer"
        }
    }
}

try:
    response = es.search(index=INDEX_NAME, body=query)
    print("Search results:")
    for hit in response["hits"]["hits"]:
        print(hit["_source"])
except NotFoundError:
    print(f"Index '{INDEX_NAME}' not found!")
