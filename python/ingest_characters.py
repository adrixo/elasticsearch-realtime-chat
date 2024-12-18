from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ConnectionError, NotFoundError
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = "elastic"
PASSWORD = "changeme"

es = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False  # Allow self-signed certificates
)

INDEX_NAME = "character_index"
if es.indices.exists(index=INDEX_NAME):
    es.indices.delete(index=INDEX_NAME)
    print(f"Index '{INDEX_NAME}' deleted successfully!")

csv_file_path = "characters_dataset.csv" 
selected_columns = ["name","description","movie","year_of_appearance"]
index_mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "description": {"type": "text"},
            "movie": {"type": "keyword"},
            "year_of_appearance": {"type": "keyword"}
        }
    }
}


df = pd.read_csv(csv_file_path, usecols=selected_columns, dtype=str)  # Load as string to handle varied data types
print(f"CSV loaded successfully with {len(df)} rows.")

# Step 2: Prepare data for bulk insertion
def generate_data(df, index_name):
    for i, row in df.iterrows():
        yield {
            "_index": index_name,
            "_id": i,  # Use row index as document ID
            "_source": row.to_dict()  # Convert each row to a dictionary
        }

if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body=index_mapping)
    print(f"Index '{INDEX_NAME}' created successfully!")
else:
    print(f"Index '{INDEX_NAME}' already exists.")

try:
    helpers.bulk(
        es, 
        generate_data(df, INDEX_NAME),
#        stats_only=True,
#        raise_on_error=True,
#        raise_on_exception=True
    )
    print("Data successfully inserted into Elasticsearch!")
except Exception as e:
    print(f"Error inserting data: {e}")

print(f"Document count in '{INDEX_NAME}': {es.count(index=INDEX_NAME)['count']}")
