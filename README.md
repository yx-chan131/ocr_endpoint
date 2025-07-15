# OCR Endpoint API

## Overview
An AI-powered FastAPI service that processes OCR text from documents and classifies the document type (e.g., medical certificate, referral letter, receipt) and extracts relevant structured fields.

## Installation & Environment Setup (Windows)
This application has been tested and verified to run successfully on the following system configuration:
```yaml
Operating System: Windows 11 Pro (64-bit)  
Processor:        Intel(R) Core(TM) i5-14400F @ 2.50 GHz  
Installed RAM:    32.0 GB 
GPU:              NVIDIA GeForce RTX 4070 Super (12GB)
```
>⚠️ **Note**: While this app may run on lower-spec machines, performance and compatibility are only guaranteed on the above configuration. A dedicated GPU is not strictly required but can help with model inference and speed if applicable.

#### ✅ Step 1: Make Sure Python 3.10 is Installed
Check if Python 3.10 is already installed:
```bash
python --version
```
If not installed, download Python 3.10 from the official site: https://www.python.org/downloads/release/python-31011/

#### ✅ Step 2: Create a Virtual Environment
Use python3.10 to create a virtual environment named `venv`:
```bash
py -3.10 -m venv venv
```

#### ✅ Step 3: Activate the Environment
On Windows:
```bash
venv\Scripts\activate
```

#### ✅ Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```




## Sample curl commands
```bash

curl -X POST "http://127.0.0.1:8000/ocr" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@data\medical_certificate.pdf"

```