from typing import Optional
from pydantic import BaseModel


class Resource(BaseModel):
    id: str
    name: str
    type: str
    transcription: Optional[str]
    shortDescription: Optional[str]
    longDescription: Optional[str]
    media: Optional[str]
    sampleSentence: Optional[str]