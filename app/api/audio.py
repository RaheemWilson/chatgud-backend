from typing import Optional
from fastapi import APIRouter, File, UploadFile, Form
from pydantic import BaseModel
import os
from urllib.request import urlopen, urlretrieve
import librosa
import ssl
import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import custom_object_scope
from tensorflow.keras.models import load_model
from keras import backend as K

router = APIRouter()

ssl._create_default_https_context = ssl._create_unverified_context


class Translation(BaseModel):
    translation: str
    confidence: Optional[float]