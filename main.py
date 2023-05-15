from fastapi import FastAPI, File, Form, UploadFile
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.schemas.audio import Evaluation
from app.utils.init_db import init_db
from app.utils.settings import get_settings
from db import db
import asyncio

from files.parse_files import parse_file

import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import custom_object_scope
from tensorflow.keras.models import load_model
from keras import backend as K
import os
from urllib.request import urlopen, urlretrieve
import ssl
from app.utils.audio import process_audio

ssl._create_default_https_context = ssl._create_unverified_context


model = None

def initialize_weights(shape, dtype=None):
    return np.random.normal(loc=0.0, scale=1e-2, size=shape)


def initialize_bias(shape, dtype=None):
    return np.random.normal(loc=0.5, scale=1e-2, size=shape)

    

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled originsss
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)

@app.on_event("startup")
async def startup():
    await db.connect()
    await init_db()
    with custom_object_scope(
        {
            "initialize_weights": initialize_weights,
            "initialize_bias": initialize_bias,
            "K": K,
        }
    ):
        global model
        model = load_model("model.h5")
    

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.get("/")
def read_root():
    return {"version": "1.0.0"}

@app.post("/audio/evaluate")
async def evaluate_audio(ref_url: str = Form(...), file: UploadFile = File(...)):
    

    audio_name = ref_url.split("/")[-1]
    ref_path = f"files/audio/{audio_name}"
    urlretrieve(ref_url, ref_path)

    test_path = f"files/audio/{file.filename}"
    with open(test_path, "wb") as f:
        f.write(await file.read())

    f.close()

    ref_audio = process_audio(ref_path)
    test_audio = process_audio(test_path)

    os.remove(ref_path)
    os.remove(test_path)

    prediction = model.predict([ref_audio, test_audio])
    prediction_score = prediction[0][0]

    print(prediction_score)
    if prediction_score <= 0.25:
        return Evaluation(prediction=1)
    elif 0.25 < prediction_score <= 0.5:
        return Evaluation(prediction=2)
    else:
        return Evaluation(prediction=3)
