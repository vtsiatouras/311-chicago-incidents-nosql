from fastapi import APIRouter

from app.api.v1.endpoints import queries, incidents, citizens

api_router = APIRouter()
api_router.include_router(queries.router, tags=['queries'])
api_router.include_router(incidents.router, tags=['incidents'])
api_router.include_router(citizens.router, tags=['citizens'])
