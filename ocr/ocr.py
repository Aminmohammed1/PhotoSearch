from paddleocr import PaddleOCR  

ocr = PaddleOCR(
    lang='en',
    text_recognition_model_name="PP-OCRv5_mobile_rec",
    use_doc_orientation_classify=True, # Use use_doc_orientation_classify to enable/disable document orientation classification model
    use_doc_unwarping=True, # Use use_doc_unwarping to enable/disable document unwarping module
    use_textline_orientation=True, # Use use_textline_orientation to enable/disable textline orientation classification model
    device="gpu:0", # Use device to specify GPU for model inference
)
def provide_ocr(path):
    result = ocr.predict(path)
    ocr_text = ''
    for res in result:  
        for stringObj in res["rec_texts"]:
            ocr_text += stringObj + '\n'
    return ocr_text
