from fastapi import APIRouter

from app.api.endpoints import scenes, login

api_router = APIRouter()
api_router.include_router(login.router, prefix="/auth/user", tags=["Login"])
api_router.include_router(scenes.router, prefix="/scenes", tags=["Scene Classification"])

