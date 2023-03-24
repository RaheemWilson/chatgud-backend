from typing import List
from fastapi import APIRouter, Depends

from app.schemas.category import Category
from db import db
router = APIRouter()

@router.get("/categories", response_model=list[Category], status_code=200)
async def get_category():
    return await db.category.find_many()