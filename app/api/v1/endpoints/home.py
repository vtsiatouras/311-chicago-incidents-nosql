from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/home", response_model=str)
def home() -> Any:
    """
    Retrieve items.
    """
    return 'Hello world!'
