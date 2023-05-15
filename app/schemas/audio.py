from pydantic import BaseModel


class Evaluation(BaseModel):
    prediction: int