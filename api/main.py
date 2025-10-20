import os
import uuid
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse , FileResponse
from descriptor.sample_run_blip import provide_description
from milvus_connection import search
from ocr.ocr import provide_ocr
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import glob

from milvus_connection import insert
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

class SearchRequest(BaseModel):
    query: str

# Directory to save uploaded images
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Metadata store file
METADATA_FILE = "image_store.json"

# In-memory store (list of dicts)
image_store = []


def load_metadata():
    """Load existing metadata from file (if present)."""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    image_store.append(record)
                except json.JSONDecodeError:
                    continue


def append_metadata(record: dict):
    """Append new metadata record to file."""
    with open(METADATA_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")


# Load existing metadata at startup
load_metadata()


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    # Generate unique ID
    image_id = str(uuid.uuid4())

    # Create unique file path
    file_extension = os.path.splitext(file.filename)[1] or ".jpg"
    file_path = os.path.join(UPLOAD_DIR, f"{image_id}{file_extension}")

    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Create record
    record = {
        "id": image_id,
        "file": {
            "path": os.path.abspath(file_path)
        },
        "name": file.filename
    }
    description = provide_description(record.get('file').get('path'))
    record['description'] = description
    ocr_text = provide_ocr(record.get('file').get('path'))
    record['ocr'] = ocr_text
    # Update in-memory + file store
    image_store.append(record)
    insert(record)
    print('data inserted in vector DB')
    append_metadata(record)

    return JSONResponse(content={"message": "Upload successful", "data": record})

@app.post("/search")
async def search_images(payload: SearchRequest):
    query = payload.query
    print(query)
    results = search(query)
    image_files = []

    for result in results:
        img_id = result.get("id")
        image_files.append({
            "id": img_id,
            "url": f"http://127.0.0.1:8000/image/{img_id}"
        })
    return JSONResponse(content={"images": image_files})


@app.get("/image/{image_id}")
async def get_image(image_id: str):
    matches = glob.glob(os.path.join(UPLOAD_DIR, f"{image_id}.*"))
    img_path = matches[0]
    ext = os.path.splitext(img_path)[1]
    img_path = os.path.join(UPLOAD_DIR, f"{image_id}{ext}")
    if not os.path.exists(img_path):
        return JSONResponse(content={"error": "Image not found"}, status_code=404)

    return FileResponse(img_path, media_type="image/jpeg")



@app.get("/images")
async def list_images():
    """List all uploaded images and their metadata."""
    return {"images": image_store}


# @app.get("/images/{image_id}")
# async def get_image_metadata(image_id: str):
#     """Retrieve metadata for a specific image by UUID."""
#     for record in image_store:
#         if record["id"] == image_id:
#             return record
#     raise HTTPException(status_code=404, detail="Image not found")


# how to run server
# ash4s@ace MINGW64 ~/Desktop/PhotoSearch (main)
# $ uvicorn api.main:app --reload