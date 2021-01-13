from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from datetime import datetime, timedelta

from app.db.db_connection import get_db
from app.models.models import FieldWithCount, ZipCodeTop3, AverageCompletionTime, ObjectIdWithTotalVotes, \
    ObjectIdWithTotalWards
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


@router.get('/average-completion-time-per-request', response_model=List[AverageCompletionTime])
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


@router.get('/most-common-service-in-bounding-box', response_model=List[FieldWithCount])
def most_common_service_in_bounding_box(
        date: datetime,
        point_a_longitude: float,
        point_a_latitude: float,
        point_b_longitude: float,
        point_b_latitude: float,
        db: Database = Depends(get_db)
) -> Any:
    """ Find the most common service request in a specified bounding box for a specific day.
    """
    cursor = db['incidents'].aggregate([
        {
            '$match': {
                '$and': [
                    {'creation_date': date},
                    {
                        'geo_location.coordinates': {
                            '$geoWithin': {
                                '$box': [
                                    [point_a_longitude, point_a_latitude],
                                    [point_b_longitude, point_b_latitude]
                                ]
                            }
                        }
                    }
                ]
            }
        },
        {
            '$project': {
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
        },
        {
            '$limit': 1
        }
    ])
    return list(cursor)


@router.get('/top-fifty-upvoted-requests', response_model=List[ObjectIdWithTotalVotes])
def top_fifty_upvoted_requests(
        date: datetime,
        db: Database = Depends(get_db)
) -> Any:
    """ Find the fifty most upvoted service requests for a specific day.
    """
    cursor = db['incidents'].aggregate([
        {
            '$match': {
                'creation_date': date
            }
        },
        {
            '$project': {
                '_id': 1,
                'total_votes': 1
            }
        },
        {
            '$sort': {
                'total_votes': -1
            }
        },
        {
            '$limit': 50
        }
    ])
    return list(cursor)


@router.get('/top-fifty-active-citizens', response_model=List[ObjectIdWithTotalVotes])
def top_fifty_active_citizens(
        db: Database = Depends(get_db)
) -> Any:
    """ Find the fifty most active citizens, with regard to the total number of upvotes.
    """
    cursor = db['citizens'].aggregate([
        {
            '$project': {
                '_id': 1,
                'total_votes': 1
            }
        },
        {
            '$sort': {
                'total_votes': -1
            }
        },
        {
            '$limit': 50
        }
    ])
    return list(cursor)


@router.get('/top-fifty-wards-citizens', response_model=List[ObjectIdWithTotalWards])
def top_fifty_wards_citizens(
        db: Database = Depends(get_db)
) -> Any:
    """ Find the top fifty citizens, with regard to the total number of wards for which they have
    upvoted an incidents.
    """
    cursor = db['citizens'].aggregate([
        {
            '$project': {
                '_id': 1,
                'total_wards': 1
            }
        },
        {
            '$sort': {
                'total_wards': -1
            }
        },
        {
            '$limit': 50
        }
    ])
    return list(cursor)
