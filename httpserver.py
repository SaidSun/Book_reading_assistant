import torch
from TeraTTS import TTS
from ruaccent import RUAccent
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import nest_asyncio
import uvicorn
import os
import soundfile as sf
import TTSModules
from TTSModules import TeraTTSClass
from preprocess_files import get_classes_from_module
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

class ModuleRequest(BaseModel):
    module_name: str

modules_dict = get_classes_from_module(TTSModules)
modules_list = list(modules_dict.keys())
print(list(modules_list))
current_module = None


app = FastAPI()
UPLOAD_DIR = "upload"
DOWNLOAD_DIR = "download"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": file.filename, "status": "uploaded"}

@app.post("/select/module")
async def upload_module(module_request: ModuleRequest):
    global current_module
    
    current_module = modules_dict[module_request.module_name]()
    
    return {
        "status": "success",
        "message": f"Модель '{current_module}' сохранена",
        "module": module_request.module_name
    }



@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, (filename+".txt"))
    if not os.path.exists(file_path):
        return {"error" : "File not found!"}
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    if not(current_module is None):
        save_path = os.path.join(DOWNLOAD_DIR, (filename+".wav"))
        current_module.generate_audio(text, save_path=save_path)
    else:
        save_path = os.path.join(DOWNLOAD_DIR, (filename+"_error.txt"))
        with open(save_path, 'w') as file:
            file.write( await "Error!")
    return FileResponse(save_path, filename="{filename}_error")

@app.get("/settings/modules")
async def get_modules_list():
     return modules_list


nest_asyncio.apply()
uvicorn.run(app, host="127.0.0.1", port=8000)