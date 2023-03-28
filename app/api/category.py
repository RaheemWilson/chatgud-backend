from typing import List
from fastapi import APIRouter

from app.schemas.category import Category
from db import db
router = APIRouter()

@router.get("/categories", response_model=List[Category], status_code=200)
async def get_category():
    return await db.category.find_many()