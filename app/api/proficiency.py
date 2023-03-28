from typing import List
from fastapi import APIRouter

from app.schemas.proficiency import Proficiency
from db import db
router = APIRouter()

@router.get("/proficiency", response_model=List[Proficiency], status_code=200)
async def get_proficiency():
    return await db.proficiency.find_many()