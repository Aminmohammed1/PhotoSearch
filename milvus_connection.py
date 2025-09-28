from pymilvus import connections
from pymilvus import FieldSchema, CollectionSchema, DataType, Collection
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim vectors
data = {"id": "0372b998-aa5b-4e76-9093-42b9467889f3", "file": {"path": "C:\\Users\\ash4s\\Desktop\\PhotoSearch\\uploads\\0372b998-aa5b-4e76-9093-42b9467889f3.jpg"}, "name": "eng1.jpg", "description": "a poster advertising a dental clinic", "ocr": "\u5de5\n\u56fd\nTIMINGS:\n10:00\nPM\n70\nTIMINGS\nAM\n11:00\nExcellent Location\nSpecialities\nAlIl\none\nDental\nServing\nDental\nNeeds\nall\nProudly\nyour\nOUR\nSERVICES:\nDental Implants\nTreatment\nRoot Canal\n\u798f\nDesigning\nSmile\nLaser Dentistry\nSurgeries\nMaxillofacial\nClear\nAligners\nBraces/\nCrown, Bridge\n&Laminates\nDentistry\nPediatric\nFor Appointment Contact:\n8074510067\n6304192605\nmagnusdentalhospital@gmail.com\nFollow us\non:\nPlot\nNo.263.\nColony, Gate\nParamount\nHills\nNo.4, Opp Lane\n\nFine\nFare\nSu\nJoerMarket,\nBeside\nELLE\nFashion Studio,\nTolichowki, Hyderabad, Telangana State.\n"}

connections.connect(
    alias="default",
    host="localhost",
    port="19530"
)

print("Connected to Milvus!")


fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=36),
    FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=1024),
    FieldSchema(name="ocr", dtype=DataType.VARCHAR, max_length=8192),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)  # depends on embedding model
]

schema = CollectionSchema(fields, description="PhotoSearch OCR+Description Collection")
collection = Collection("photo_search", schema)
#####################
text_to_embed = f"{data['description']} {data['ocr']}"
vector = model.encode(text_to_embed).tolist()
##isert
collection.insert([
    [data["id"]],              # list of ids
    [data["description"]],     # list of descriptions
    [data["ocr"]],             # list of OCR texts
    [vector]                   # list of embeddings
])
collection.flush()

collection.load()

##search
query = "Find dental clinic posters"
query_vector = model.encode(query).tolist()

results = collection.search(
    data=[query_vector],
    anns_field="embedding",
    param={"metric_type": "COSINE", "params": {"nprobe": 10}},
    limit=3,
    output_fields=["id", "description", "ocr"]
)

for hit in results[0]:
    print(f"ID: {hit.entity.get('id')} | Score: {hit.distance}")
    print(f"Description: {hit.entity.get('description')}")
    print(f"OCR Snippet: {hit.entity.get('ocr')[:100]}...\n")

##

collection.create_index(
    field_name="embedding",
    index_params={"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
)

