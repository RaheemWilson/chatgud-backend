from fastapi import APIRouter, Depends
from app.api.auth import router as auth_router
from app.api.proficiency import router as proficiency_router
from app.api.category import router as category_router
from app.utils.auth import get_current_user

api_router = APIRouter(prefix='/api')
api_router.include_router(router=auth_router, prefix='/auth', tags=["Auth"])
api_router.include_router(router=proficiency_router, tags=["Proficiency"])
api_router.include_router(router=category_router, tags=["Category"], dependencies=[Depends(get_current_user)])