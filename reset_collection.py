from pymilvus import connections, utility

# Connect to Milvus
connections.connect(alias="default", host="localhost", port="19530")

# Drop the collection if it exists
if utility.has_collection("photo_search"):
    print("Dropping existing collection...")
    utility.drop_collection("photo_search")
    print("Collection dropped successfully!")
else:
    print("No existing collection found.")