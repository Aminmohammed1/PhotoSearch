# PhotoSearch
## OCR setup:
cpu:
python -m pip install paddlepaddle==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
python -m pip install paddleocr
verify:
    paddleocr text_recognition \
        --model_name PP-OCRv5_mobile_rec \
        -i https://cdn-uploads.huggingface.co/production/uploads/681c1ecd9539bdde5ae1733c/2PZfbirjfxA88695lRmgk.jpeg
paddleocr ocr -i https://cdn-uploads.huggingface.co/production/uploads/681c1ecd9539bdde5ae1733c/3ul2Rq4Sk5Cn-l69D695U.png \
    --text_recognition_model_name PP-OCRv5_mobile_rec \
    --use_doc_orientation_classify False \
    --use_doc_unwarping False \
    --use_textline_orientation True \
    --save_path ./output

gpu:
##### for CUDA12.6
python -m pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
python -m pip install paddleocr
python ocr.py