from pydantic import BaseModel


class Proficiency(BaseModel):
    id: str
    name: str
    description: str
    preferenceOrder: int