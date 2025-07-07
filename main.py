import io
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from utils.utils_data import *

# Use environment variable to set debug mode
DEBUG_MODE = os.getenv("DEBUG", "0") == "1"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI for medical documentation"}

@app.post("/ocr")
async def upload_file(file: UploadFile = File(...)):
    # Check MIME type or extension
    if not is_valid_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type {file.filename}. Only jpg, jpeg, png, bmp, and pdf are allowed."
        )        

    imname = os.path.splitext(file.filename)[0]
    
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    
    img = read_data_to_image(contents, file.filename.endswith(".pdf"))

    if DEBUG_MODE:
        save_name = f"{imname}.png"
        save_path = os.path.join(".\debug", save_name)
        cv2.imwrite(save_path, img[..., ::-1])
    
    # Todo: Call the OCR process function (stubbed for now)
    result = {"message": f"{file.filename} is valid"}
    
    return JSONResponse(content=result)
