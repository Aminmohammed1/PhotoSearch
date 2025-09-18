# 📷 PhotoSearch – OCR Setup
CPU Setup
### Install PaddlePaddle (CPU version)
python -m pip install paddlepaddle==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

### Install PaddleOCR
python -m pip install paddleocr

Verify Installation
### Basic text recognition test
paddleocr text_recognition \
  --model_name PP-OCRv5_mobile_rec \
  -i https://cdn-uploads.huggingface.co/production/uploads/681c1ecd9539bdde5ae1733c/2PZfbirjfxA88695lRmgk.jpeg

### OCR on another sample image
paddleocr ocr \
  -i https://cdn-uploads.huggingface.co/production/uploads/681c1ecd9539bdde5ae1733c/3ul2Rq4Sk5Cn-l69D695U.png \
  --text_recognition_model_name PP-OCRv5_mobile_rec \
  --use_doc_orientation_classify False \
  --use_doc_unwarping False \
  --use_textline_orientation True \
  --save_path ./output

GPU Setup (CUDA 12.6)
### Install PaddlePaddle (GPU version for CUDA 12.6)
python -m pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/

### Install PaddleOCR
python -m pip install paddleocr

### Run OCR script
python ocr.py
