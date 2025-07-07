import os
import cv2
import numpy as np
from paddleocr import PaddleOCR

class OCR():
    def __init__(self):
        self.ocr = PaddleOCR(
                lang="en",
                use_doc_orientation_classify=False, 
                use_doc_unwarping=False, 
                use_textline_orientation=False) # text detection + text recognition

    def predict(self, img: np.ndarray, savename: str) -> str:
        result = self.ocr.predict(img)[0]
        result.save_to_img(f".\debug\\{savename}")  
        texts = result['rec_texts']
        out_str = " ".join(texts)

        return out_str


if __name__ == "__main__":    
    impath = r"D:\Code\ocr_endpoint\debug\medical_certificate.png"
    imname = os.path.splitext(os.path.basename(impath))[0]

    ocr = OCR()

    img = cv2.imread(impath)[..., ::-1]
    out_str = ocr.predict(img, imname)
    print(out_str)
