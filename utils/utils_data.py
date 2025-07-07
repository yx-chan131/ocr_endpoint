import os
import io
import cv2
import numpy as np
from PIL import Image
from pdf2image import pdf2image

# Supported file extensions
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "pdf"}

def is_valid_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower().replace(".", "")
    return ext in ALLOWED_EXTENSIONS

def is_valid_filepath(filepath: str) -> bool:
    return os.path.exists(filepath)

def read_data_to_image(contents: bytes, pdf: bool = False):
    if not pdf:
        img = Image.open(io.BytesIO(contents))
        img = np.asarray(img)
    else:
        img = pdf2image.convert_from_bytes(contents, dpi=200, poppler_path=os.getenv("POPPLER_PATH"))[0]
        img = np.asarray(img)

    return img
