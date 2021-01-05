from typing import Any
from fastapi import APIRouter, Depends
from pymongo.database import Database

from app.db.db_connection import get_db


router = APIRouter()


@router.get("/home", response_model=str)
def home(db: Database = Depends(get_db)) -> Any:
    """ Home page endpoint
    """
    return 'Hello world!'
