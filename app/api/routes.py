from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.proficiency import router as proficiency_router

api_router = APIRouter(prefix='/api')
api_router.include_router(router=auth_router, prefix='/auth', tags=["Auth"])
api_router.include_router(router=proficiency_router, tags=["Proficiency"])