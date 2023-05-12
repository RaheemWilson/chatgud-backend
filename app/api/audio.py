from typing import Optional
from fastapi import APIRouter, File, UploadFile, Form
from pydantic import BaseModel
import os
from urllib.request import urlopen, urlretrieve
import librosa
import requests
import ssl
import pickle

router = APIRouter()

ssl._create_default_https_context = ssl._create_unverified_context

class Translation(BaseModel):
    translation: str
    confidence: Optional[float]

@router.post("/evaluate", response_model=Translation, status_code=200)
async def evaluate_audio(ref_url: str = Form(...), file: UploadFile = File(...)):
    audio_name = ref_url.split("/")[-1]
    audio_path = f"files/audio/{audio_name}"
    urlretrieve(ref_url, audio_path)
    
    file_path = f"files/audio/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    ref_audio, sr = librosa.load(audio_path)
    test_audio, sr_file = librosa.load(file_path)
    
    os.remove(audio_path)
    os.remove(file_path)
    model = None
    with open("model.pkl", 'rb') as f:
        print("found")
        # model = pickle.load(f)
        
    return Translation(translation=file.filename)


# file_location = f"files/{file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(file.file.read())