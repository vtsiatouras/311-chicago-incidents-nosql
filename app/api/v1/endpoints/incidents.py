from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from app.db.db_connection import get_db
from app.models.models import Incident, IncidentCreate, DocumentID

router = APIRouter()


@router.post('/create-incident', response_model=DocumentID)
def create_incident(
        *,
        incident_in: IncidentCreate,
        db: Database = Depends(get_db)
) -> Any:
    """ Create a new incident
    """
    object_id = db['incidents'].insert_one(incident_in.dict(by_alias=True))
    return {'_id': object_id.inserted_id}


@router.get('/get-incident', response_model=Incident)
def get_incident(
        incident_id: str,
        db: Database = Depends(get_db)
) -> Any:
    """ Get an incident
    """
    try:
        incident_id_obj = ObjectId(incident_id)
    except InvalidId:
        raise HTTPException(
            status_code=422,
            detail=f"'{incident_id}' is not a valid incident ID, "
                   f"it must be a 12-byte input or a 24-character hex string",
            headers={'X-Error': 'Validation Error'},
        )

    incident = db['incidents'].find_one({'_id': incident_id_obj})

    if incident:
        return incident
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Incident with id '{incident_id}' was not found",
            headers={'X-Error': 'Not Found Error'},
        )
