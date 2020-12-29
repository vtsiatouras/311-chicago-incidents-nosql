from fastapi import APIRouter

from app.api.v1.endpoints import home

api_router = APIRouter()
api_router.include_router(home.router, tags=["home"])
