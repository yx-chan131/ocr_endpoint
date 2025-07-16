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
Use python3.10 to create a virtual environment named `venv` under the project directory:
```bash
cd path/to/your/code/directory
py -3.10 -m venv venv
```

#### ✅ Step 3: Activate the Environment
On Windows:
```bash
venv\Scripts\activate
```

#### ✅ Step 4: Install Dependencies
This project uses [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) for Optical Character Recognition. Before installing **requirements.txt**, you must install **PaddlePaddle**, which is a required backend library for PaddleOCR. 
```bash
# Installation for CPU
python -m pip install paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

# Installation for GPU
# Refer to https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/develop/install/pip/windows-pip.html
# For example, Windows OS + CUDA12.6:
python -m pip install paddlepaddle-gpu==3.1.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
```

Install other dependencies:
```bash
pip install -r requirements.txt
```

#### ✅ Step 5: Environment Configuration
Before running the app, you need to create a `.env` file in the project root directory to store environment variables.
Create a file named `.env` (no filename prefix) and add the following content:
```env
DEBUG=1
POPPLER_PATH="D:\\Code\\ocr_endpoint\\utils\\poppler\\poppler-24.08.0\\Library\\bin"
OPENAI_API_KEY="your openai api key"
```
| Variable         | Description                                                                                          |
|------------------|------------------------------------------------------------------------------------------------------|
| `DEBUG`          | Set to `1` to **enable debug mode**: intermediate OCR visualization results will be saved to `debug/`. In addition, LangChain verbose mode will be set to True, and the OCR result will be printed to the console. Set to `0` to disable debug mode. |
| `POPPLER_PATH`   | Required for `pdf2image` to convert PDF files. This should point to the `bin` folder inside your Poppler installation. |
| `OPENAI_API_KEY` | Your API key for calling OpenAI endpoints.            |

## Start the Application & Test the API
#### Run the FastAPI app
Make sure your virtual environment is activated, then start the API using `uvicorn`
```bash
cd path/to/your/code/directory
# option 1: Production Mode
uvicorn main:app
# option 2: Development Mode
uvicorn main:app --reload
```
If the server starts successfully, you'll see output like
```pgsql
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
####  Test the Endpoint
```bash
curl -X POST "http://127.0.0.1:8000/ocr" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@{path to document}"

# example: test medical_certificate.pdf placed in data subfolder
curl -X POST "http://127.0.0.1:8000/ocr" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@data\medical_certificate.pdf"

```