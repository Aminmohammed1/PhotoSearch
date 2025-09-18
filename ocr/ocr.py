from paddleocr import PaddleOCR  

ocr = PaddleOCR(
    lang='en',
    text_recognition_model_name="PP-OCRv5_mobile_rec",
    use_doc_orientation_classify=True, # Use use_doc_orientation_classify to enable/disable document orientation classification model
    use_doc_unwarping=True, # Use use_doc_unwarping to enable/disable document unwarping module
    use_textline_orientation=True, # Use use_textline_orientation to enable/disable textline orientation classification model
    device="gpu:0", # Use device to specify GPU for model inference
)
result = ocr.predict("./ss-png.png")  
for res in result:  
    print(res["rec_texts"])
