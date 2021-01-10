from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from datetime import datetime, timedelta

from app.db.db_connection import get_db
from app.models.models import FieldWithCount, ZipCodeTop3, AverageCompletionTime
from app.schemas.schemas import TypeOfServiceRequest

router = APIRouter()


@router.get('/total-requests-per-type', response_model=List[FieldWithCount])
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
            headers={'X-Error': 'Validation Error'},
        )

    cursor = db['incidents'].aggregate([
        {
            '$match': {
                'creation_date': {'$gte': start_date, '$lte': end_date}
            }
        },
        {
            '$project': {
                '_id': 1,
                'type_of_service_request': 1
            }
        },
        {
            '$group': {
                '_id': '$type_of_service_request',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {
                'count': -1
            }
        }
    ])
    return list(cursor)


@router.get('/total-requests-per-day', response_model=List[FieldWithCount])
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
            headers={'X-Error': 'Validation Error'},
        )

    cursor = db['incidents'].aggregate([
        {
            '$match': {
                '$and': [
                    {'type_of_service_request': request_type},
                    {'creation_date': {'$gte': start_date, '$lte': end_date}}
                ]
            }
        },
        {
            '$project': {
                '_id': 1, 'creation_date': 1
            }
        },
        {
            '$group': {
                '_id': '$creation_date',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {
                '_id': -1
            }
        }
    ])
    return list(cursor)


@router.get('/three-most-common-requests-per-zipcode', response_model=List[ZipCodeTop3])
def three_most_common_requests_per_zipcode(
        date: datetime,
        db: Database = Depends(get_db)
) -> Any:
    """ Find the three most common service requests per zipcode for a specific day.
    """
    cursor = db['incidents'].aggregate([
        {
            '$match': {'creation_date': date}
        },
        {
            '$project': {
                'type_of_service_request': 1,
                'zip_code': 1
            }
        },
        {   # Create counts per type and zipcode
            '$group': {
                '_id': {
                    'type_of_service_request': '$type_of_service_request',
                    'zip_code': '$zip_code'
                },
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {
                '_id.zip_code': 1, 'count': -1
            }
        },
        {   # Group types & counts per zipcode inside an array
            '$group': {
                '_id': '$_id.zip_code',
                'counts': {
                    '$push': {
                        'type_of_service_request': '$_id.type_of_service_request',
                        'count': '$count'
                    }
                }
            }
        },
        {    # Select first 3 elements of each array
            '$project': {
                'top_three': {'$slice': ['$counts', 3]}}
        }
    ])
    return list(cursor)


@router.get('/three-least-common-wards', response_model=List[FieldWithCount])
def three_least_common_wards(
        request_type: TypeOfServiceRequest,
        db: Database = Depends(get_db)
) -> Any:
    """ Find the three least common wards with regards to a given service request type.
    """
    cursor = db['incidents'].aggregate([
        {
            '$match': {
                '$and': [
                    {'type_of_service_request': request_type},
                    {'ward': {'$exists': 'true'}}       # Exclude records with no ward
                ]
            }
        },
        {
            '$project': {
                'ward': 1
            }
        },
        {
            '$group': {
                '_id': '$ward',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {
                'count': 1
            }
        },
        {
            '$limit': 3
        }
    ])
    return list(cursor)


@router.get('/average-completion-time-per-request', response_model=Any)
def average_completion_time_per_request(
        start_date: datetime,
        end_date: datetime,
        db: Database = Depends(get_db)
) -> Any:
    """ Find the average completion time per service request for a specific date range.
    """
    cursor = db['incidents'].aggregate([
        {
            '$match': {
                '$and': [
                    {'creation_date': {'$gte': start_date, '$lte': end_date}},
                    {'creation_date': {'$exists': 'true'}},
                    {'completion_date': {'$exists': 'true'}}
                ]
            }
        },
        {
            '$project': {
                'creation_date': 1,
                'completion_date': 1,
                'type_of_service_request': 1
            }
        },
        {
            '$group': {
                '_id': '$type_of_service_request',
                'average_completion_time': {
                    '$avg': {
                        '$subtract': [
                            '$completion_date', '$creation_date'
                        ]
                    }
                }
            }
         },
        {
            '$sort': {
                '_id': 1
            }
        }
    ])
    # Normalize average times
    result = []
    for elem in cursor:
        elem['average_completion_time'] = str(timedelta(milliseconds=elem['average_completion_time']))
        result.append(elem)
    return result

