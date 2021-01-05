from fastapi import APIRouter

from app.api.v1.endpoints import home, queries

api_router = APIRouter()
api_router.include_router(home.router, tags=["home"])
api_router.include_router(queries.router, tags=["queries"])
