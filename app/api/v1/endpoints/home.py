from typing import Any
from fastapi import APIRouter

from app.db import db_connection

router = APIRouter()


@router.get("/home", response_model=str)
def home() -> Any:
    """
    Retrieve items.
    """
    docs = db_connection.db.incidents.find()
    for doc in docs:
        print(doc)
    return 'Hello world!'
