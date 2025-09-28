from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import os
print("Current working directory:", os.getcwd())

# 1. Load BLIP model + processor (downloads weights on first run)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# 2. Load an image
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# IMAGE_PATH = os.path.join(SCRIPT_DIR, "../ocr/ss-png.png")

# print(f"Loading image from: {IMAGE_PATH}")
# image = Image.open(IMAGE_PATH)

# # 3. Generate caption
# inputs = processor(images=image, return_tensors="pt")
# caption_ids = model.generate(**inputs, max_new_tokens=30)
# caption = processor.decode(caption_ids[0], skip_special_tokens=True)

# print("Generated Caption:", caption)

def provide_description(path):
    image = Image.open(path)
    inputs = processor(images=image, return_tensors="pt")
    caption_ids = model.generate(**inputs, max_new_tokens=30)
    description = processor.decode(caption_ids[0], skip_special_tokens=True)
    return description


