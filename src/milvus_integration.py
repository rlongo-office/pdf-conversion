from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import json

# Connect to Milvus
connections.connect(
    alias="default",
    host="useast.services.cloud.techzone.ibm.com",
    port="35034",
    secure=True,
    client_key_path="",        # Leave blank to skip
    client_pem_path="",        # Leave blank to skip
    server_pem_path="",        # Leave blank to skip
    server_name="",
    tls_verify=False           # This disables SSL verification
)

def create_milvus_collection(collection_name="docling_vectors", dim=512):
    """
    Create a Milvus collection if it doesn't exist.

    Args:
        collection_name (str): Name of the collection.
        dim (int): Dimension of the vector data.
    """
    existing_collections = [c.name for c in Collection.list()]
    if collection_name in existing_collections:
        print(f"Collection '{collection_name}' already exists.")
        return Collection(collection_name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=1000),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]
    schema = CollectionSchema(fields, description="Docling extracted vectors")
    collection = Collection(name=collection_name, schema=schema)
    print(f"Collection '{collection_name}' created.")
    return collection

def convert_text_to_vector(text):
    """
    Placeholder function to convert text to vector.
    Replace this with actual Docling or embedding model logic.
    """
    import numpy as np
    return np.random.rand(512).tolist()  # Simulated 512-dim vector

def insert_data_to_milvus(json_path, collection_name="docling_vectors"):
    """
    Insert JSON data into Milvus.

    Args:
        json_path (str): Path to the JSON file.
        collection_name (str): Milvus collection name.
    """
    collection = create_milvus_collection(collection_name)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Assuming 'content' contains the text to be vectorized
    documents = data.get("pages", [])

    for idx, doc in enumerate(documents):
        content = doc.get("text", "")
        if content.strip():
            embedding = convert_text_to_vector(content)
            collection.insert([[idx], [content], [embedding]])

    print(f"Inserted {len(documents)} documents into Milvus collection '{collection_name}'.")
    return len(documents)

def search_in_milvus(query_vector, collection_name="docling_vectors", limit=5):
    """
    Search for similar vectors in Milvus.

    Args:
        query_vector (list): The query vector for similarity search.
        collection_name (str): Milvus collection name.
        limit (int): Number of results to return.
    """
    collection = Collection(collection_name)
    collection.load()

    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(
        data=[query_vector],
        anns_field="embedding",
        param=search_params,
        limit=limit
    )

    for hits in results:
        for hit in hits:
            print(f"ID: {hit.id}, Distance: {hit.distance}, Content: {hit.entity.get('content')}")

    return results
