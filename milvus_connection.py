from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from sentence_transformers import SentenceTransformer

# 1. Connect to Milvus
try:
    connections.connect(alias="default", host="localhost", port="19530")
    print("Connected to Milvus!")
except Exception as e:
    print('error occured while trying to connect to Milvus')

# 2. Define schema
fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=36),
    FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=1024),
    FieldSchema(name="ocr", dtype=DataType.VARCHAR, max_length=8192),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)  # all-MiniLM-L6-v2 uses 384 dimensions
]
schema = CollectionSchema(fields, description="PhotoSearch OCR+Description Collection")

# 3. Create or load collection
collection_name = "photo_search"
if utility.has_collection(collection_name):
    collection = Collection(collection_name)
    print(f"Loaded existing collection: {collection_name}")
else:
    collection = Collection(name=collection_name, schema=schema)
    print(f"Created new collection: {collection_name}")

# 4. Ensure index exists (only once per collection/field)
index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "COSINE",
    # "params": {"nlist": 128}
    "params": {"M": 32, "efConstruction": 200}
}

indexes = collection.indexes
if not indexes:  # no index exists yet
    print("Creating index on 'embedding' field...")
    collection.create_index(field_name="embedding", index_params=index_params)
else:
    print("Index already exists, skipping creation.")

# 5. Insert some example data
# model = SentenceTransformer("all-MiniLM-L6-v2")
# model = SentenceTransformer("BAAI/bge-large-en-v1.5")
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder

model = SentenceTransformer('all-MiniLM-L6-v2')  # Smaller, reliable model
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def normalize(v):
    v = np.array(v)
    return (v / np.linalg.norm(v)).tolist()

# def insert(data):
#     text_to_embed = f"Description: {data['description']} OCR: {data['ocr']}"
#     vector = model.encode(text_to_embed).tolist()
#     collection.insert([
#         [data["id"]],
#         [data["description"]],
#         [data["ocr"]],
#         [vector]
#     ])
#     collection.flush()

#     # 6. Load collection into memory (needed every run before searching)
#     collection.load()
def insert(data):
    # Combine description and OCR text in a more natural way
    text_to_embed = f"{data['description']}. {data['ocr']}" if data['ocr'] else data['description']
    vector = normalize(model.encode(text_to_embed))
    collection.insert([
        [data["id"]],
        [data["description"]],
        [data["ocr"]],
        [vector]
    ])
    collection.flush()
    collection.load()

# def search(query):
#     query_vector = model.encode(query).tolist()
#     results = collection.search(
#         data=[query_vector],
#         anns_field="embedding",
#         # param={"metric_type": "COSINE", "params": {"nprobe": 32}},
#         param={"metric_type": "COSINE", "params": {"ef": 64}},
#         limit=10,
#         output_fields=["id", "description", "ocr"]
#     )
#     result = []
#     for hit in results[0]:
#         temp = {}
#         temp['id'] = hit.entity.get('id')
#         temp['score'] = hit.distance
#         temp['description'] = hit.entity.get('description')
#         temp['ocr'] = hit.entity.get('ocr')
#         result.append(temp)
#     return result

def rerank(query, results):
    if not results:
        return []
    pairs = [(query, f"{r['description']} {r['ocr']}") for r in results]
    scores = reranker.predict(pairs)
    for i, r in enumerate(results):
        r['relevance'] = float(scores[i])
    # Higher score = more relevantl
    return sorted(results, key=lambda x: x['relevance'], reverse=True)
def search(query):
    # Use the query directly without additional formatting
    query_vector = normalize(model.encode(query))
    results = collection.search(
        data=[query_vector],
        anns_field="embedding",
        param={"metric_type": "COSINE", "params": {"ef": 128}},
        limit=20,
        output_fields=["id", "description", "ocr"]
    )

    raw_results = [
        {
            "id": hit.entity.get("id"),
            "score": hit.distance,
            "description": hit.entity.get("description"),
            "ocr": hit.entity.get("ocr")
        }
        for hit in results[0]
    ]

    # Re-rank top results for precision
    return rerank(query, raw_results)[:10]

# data = {
#     "id": "0372b998-aa5b-4e76-9093-42b9467889f3",
#     "file": {"path": "C:\\Users\\ash4s\\Desktop\\PhotoSearch\\uploads\\0372b998-aa5b-4e76-9093-42b9467889f3.jpg"},
#     "name": "eng1.jpg",
#     "description": "a poster advertising a dental clinic",
#     "ocr": "Dental Implants, Root Canal, Smile Designing..."
# }
# text_to_embed = f"{data['description']} {data['ocr']}"
# vector = model.encode(text_to_embed).tolist()

# collection.insert([
#     [data["id"]],
#     [data["description"]],
#     [data["ocr"]],
#     [vector]
# ])
# collection.flush()

# # 6. Load collection into memory (needed every run before searching)
# collection.load()

# # 7. Search
# query = "Find dental clinic posters"
# query_vector = model.encode(query).tolist()

# results = collection.search(
#     data=[query_vector],
#     anns_field="embedding",
#     param={"metric_type": "COSINE", "params": {"nprobe": 10}},
#     limit=3,
#     output_fields=["id", "description", "ocr"]
# )

# print("\n--- Search Results ---")
# for hit in results[0]:
#     print(f"ID: {hit.entity.get('id')} | Score: {hit.distance:.4f}")
#     print(f"Description: {hit.entity.get('description')}")
#     print(f"OCR Snippet: {hit.entity.get('ocr')[:100]}...\n")