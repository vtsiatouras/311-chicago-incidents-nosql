from typing import Any, List
from fastapi import APIRouter, Query, Depends, HTTPException
from pymongo.database import Database
from datetime import datetime

from app.db.db_connection import get_db
from app.models.models import FieldWithCount
from app.schemas.schemas import TypeOfServiceRequest

router = APIRouter()


@router.get("/total-requests-per-type", response_model=List[FieldWithCount])
def total_requests_per_type(
        start_date: datetime,
        end_date: datetime,
        db: Database = Depends(get_db)
) -> Any:
    """ Find the total requests per type that were created within a specified time range and sort
    them in a descending order.
    """
    if end_date < start_date:
        raise HTTPException(
            status_code=422,
            detail="'start_date' must be less than 'end_date'",
            headers={"X-Error": "Validation Error"},
        )

    cursor = db['incidents'].aggregate([
        {"$match": {"creation_date": {"$gte": start_date, "$lte": end_date}}},
        {"$project": {"_id": 1, "type_of_service_request": 1}},
        {"$group": {"_id": "$type_of_service_request", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])
    return list(cursor)


@router.get("/total-requests-per-day", response_model=List[FieldWithCount])
def total_requests_per_day(
        start_date: datetime,
        end_date: datetime,
        request_type: TypeOfServiceRequest,
        db: Database = Depends(get_db)
) -> Any:
    """ Find the number of total requests per day for a specific request type and time range.
    """
    if end_date < start_date:
        raise HTTPException(
            status_code=422,
            detail="'start_date' must be less than 'end_date'",
            headers={"X-Error": "Validation Error"},
        )

    cursor = db['incidents'].aggregate([
        {"$match": {"$and": [{"type_of_service_request": request_type},
                             {"creation_date": {"$gte": start_date, "$lte": end_date}}]}},
        {"$project": {"_id": 1, "creation_date": 1}},
        {"$group": {"_id": "$creation_date", "count": {"$sum": 1}}},
        {"$sort": {"_id": -1}}
    ])
    # print(list(cursor))
    return list(cursor)
