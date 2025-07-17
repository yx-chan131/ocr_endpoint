import warnings
warnings.filterwarnings("ignore")

import cv2
import json
import time

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse

from ai_agent import create_ai_agent
from utils.utils_data import *
from utils.util_ocr import OCR, SignatureDetection

load_dotenv()

# Use environment variable to set debug mode
DEBUG_MODE = os.getenv("DEBUG", "0") == "1"

t1 = time.time()
print("Modules loading...")
OCRModel = OCR()
SignDetect = SignatureDetection()
agent = create_ai_agent(os.getenv("OPENAI_API_KEY"), verbose=DEBUG_MODE)
t2 = time.time()
print(f"Modules loading done! ({round(t2-t1,2)}s)")

if DEBUG_MODE:
    os.makedirs(".\\debug", exist_ok=True)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI for medical documentation extraction"}

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    content = json.dumps(
            {
            "HTTP Error": exc.status_code,
            "error": exc.detail
            },
            indent=2
            )
    return JSONResponse(
        status_code=exc.status_code,
        content=json.loads(content),
    )

@app.post("/ocr")
async def upload_file(file: UploadFile = File(...)):
    t1 = time.time()
    
    # Check MIME type or extension
    allowed_types = ["image/jpeg", "image/png", "image/bmp", "application/pdf"]
    if file.content_type not in allowed_types:
    # if not is_valid_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"unsupported_file_type"
        )        

    imname = os.path.splitext(file.filename)[0]
    
    contents = await file.read()
    if not contents:
        raise HTTPException(
            status_code=400, 
            detail="file_missing"
        )
    
    try: 
        img = read_data_to_image(contents, file.filename.endswith(".pdf"))

        result_dict = {}    

        if DEBUG_MODE:
            save_name = f"{imname}.png"
            save_path = os.path.join(".\debug", save_name)
            cv2.imwrite(save_path, img[..., ::-1])
        
        # Call the OCR process function
        out_str, _ = OCRModel.predict(img[..., ::-1], DEBUG_MODE, imname)
        if not out_str:
            raise HTTPException(
                status_code=422, 
                detail="unsupported_document_type"
            )        
        
        agent_out = agent.run(out_str)    
        

        if "document_type" not in agent_out.lower() and "false" in agent_out.lower():
            raise HTTPException(
                status_code=422, 
                detail="unsupported_document_type"
            )
        else:        
            data = json.loads(agent_out)
        
        document_type = data.pop("document_type")

        if document_type == "referral_letter":
            signPresence = SignDetect.predict(img[..., ::-1].copy(), DEBUG_MODE, imname)
            data["signature_presence"] = signPresence

        # check provider_name
        provider_name = data.get("provider_name")
        if isinstance(provider_name, str):
            normalized = provider_name.replace(" ", "").lower()
            if "fullertonhealth" in normalized:
                data["provider_name"] = None

        t2 = time.time()

        result_dict["message"] = "Processing completed."
        # result_dict["result_OCR"] = out_str
        result_dict["result"] = {}
        result_dict["result"]["document_type"] = document_type
        result_dict["result"]["total_time"] = round(t2 - t1, 2)
        result_dict["result"]["finalJson"] = data

        content = json.dumps(result_dict, indent=2)    
        return JSONResponse(content=json.loads(content))
    
    except HTTPException as e:
        raise e  # re-raise custom errors

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="internal_server_error"
        )