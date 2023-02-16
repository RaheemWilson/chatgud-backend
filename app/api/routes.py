from fastapi import APIRouter
from app.api.auth import router as auth_router

api_router = APIRouter(prefix='/api')
api_router.include_router(router=auth_router, prefix='/auth', tags=["Auth"])