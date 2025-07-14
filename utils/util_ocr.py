import os
import cv2
import numpy as np
import supervision as sv
from paddleocr import PaddleOCR
from ultralytics import YOLO
from huggingface_hub import hf_hub_download

class OCR():
    def __init__(self):
        self.ocr = PaddleOCR(
                lang="en",
                use_doc_orientation_classify=False, 
                use_doc_unwarping=False, 
                use_textline_orientation=False) # text detection + text recognition


    def predict(self, img: np.ndarray, debug: bool, savename: str) -> str:
        result = self.ocr.predict(img)[0]
        if debug:
            result.save_to_img(f".\debug\\{savename}")  
        texts = result['rec_texts']
        out_str = " ".join(texts)
        print(f"First round: {out_str}")
        print(len(out_str))

        if len(out_str) < 1:
            return out_str, img

        boxes = result['rec_boxes']
        x1 = int(np.min(boxes[:, 0]))
        y1 = int(np.min(boxes[:, 1]))
        x2 = int(np.max(boxes[:, 2]))
        y2 = int(np.max(boxes[:, 3]))

        img = img[y1:y2, x1:x2, :]
        result = self.ocr.predict(img)[0]
        if debug:
            result.save_to_img(f".\debug\\{savename}")  
        texts = result['rec_texts']
        out_str = " ".join(texts)
        print(f"Second round: {out_str}")
        print(len(out_str))

        return out_str, img

class SignatureDetection():
    def __init__(self):
        # https://huggingface.co/tech4humans/yolov8s-signature-detector
        model_path = r".\utils\\models\\yolov8s.pt"
        self.model = YOLO(model_path)
        self.box_annotator = sv.BoxAnnotator()
        self.thres = 0.65

    def predict(self, img: np.ndarray, debug: bool, savename: str) -> bool:
        results = self.model(img)        

        conf = results[0].boxes.conf.numpy()
        if debug:
            print("Model Confidence:", conf)
            detections = sv.Detections.from_ultralytics(results[0])
            detections.xyxy = detections.xyxy.astype(np.uint16)
            annotated_image = self.box_annotator.annotate(scene=img, detections=detections) 
            save_path = f".\debug\\{savename}_signResult.jpg"
            cv2.imwrite(save_path, annotated_image)

        if len(conf) < 1:
            return False
        else:
            # if conf.max() > 0.65:
            if conf.max() > 0.3:
                return True
            else:
                return False

        

if __name__ == "__main__":    
    # impath = r"D:\Code\ocr_endpoint\debug\medical_certificate.png"
    impath = r"D:\Code\ocr_endpoint\debug\medical_certificate_whitecoat.png"
    imname = os.path.splitext(os.path.basename(impath))[0]
    
    img = cv2.imread(impath)
    signDetect = SignatureDetection()
    signDetect.predict(img, True, imname)

    # ocr = OCR()
    # out_str, _ = ocr.predict(img, True, imname)
    # print(out_str)

    
