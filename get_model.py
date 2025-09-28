from sentence_transformers import SentenceTransformer
import os

# Choose a folder to store the model
MODEL_DIR = os.path.join(os.getcwd(), "models", "all-MiniLM-L6-v2")
os.makedirs(MODEL_DIR, exist_ok=True)

# Download and save the model locally
print(f"⬇️ Downloading 'all-MiniLM-L6-v2' to {MODEL_DIR} ...")
model = SentenceTransformer("all-MiniLM-L6-v2")
model.save(MODEL_DIR)

print("✅ Model downloaded and saved locally!")
