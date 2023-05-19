from fastapi import APIRouter, Depends
from app.api.auth import router as auth_router
from app.api.proficiency import router as proficiency_router
from app.api.category import router as category_router
from app.api.user import router as user_router
from app.api.task import router as task_router
from app.api.audio import router as audio_router
from app.api.activities import router as activities_router
from app.utils.auth import get_current_user

api_router = APIRouter(prefix='/api')
api_router.include_router(router=auth_router, prefix='/auth', tags=["Auth"])
api_router.include_router(router=proficiency_router, tags=["Proficiency"])
api_router.include_router(router=category_router, tags=["Category"], dependencies=[Depends(get_current_user)])
api_router.include_router(router=user_router, tags=["User"])
api_router.include_router(router=task_router, tags=["Task"])
# api_router.include_router(router=audio_router, prefix='/audio', tags=["Audio"], dependencies=[Depends(get_current_user)])
api_router.include_router(router=activities_router, prefix='/activities', tags=["Activities"])
