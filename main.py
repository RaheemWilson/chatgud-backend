from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.utils.init_db import init_db
from app.utils.settings import get_settings
from db import db
import asyncio

from files.parse_files import parse_file

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)

@app.on_event("startup")
async def startup():
    await db.connect()
    await init_db()
    

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.get("/")
def read_root():
    return {"version": "1.0.0"}