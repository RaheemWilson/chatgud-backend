from typing import Optional
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from db import db

router = APIRouter()

class Translation(BaseModel):
    translation: str
    confidence: Optional[float]

@router.post("/translate", response_model=Translation, status_code=200)
def translate_audio(sound: UploadFile):
    return Translation(translation=sound.filename)

@router.post("/evaluate", response_model=Translation, status_code=200)
def evaluate_audio(file: UploadFile = File(...)):
    # file_location = f"files/{file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(file.file.read())
    return Translation(translation=file.filename)