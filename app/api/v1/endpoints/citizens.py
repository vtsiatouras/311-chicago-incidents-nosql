from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException
from pymongo import ReturnDocument
from pymongo.database import Database

from app.db.db_connection import get_db
from app.models.models import CitizenCreateVote, DocumentID

router = APIRouter()


@router.post('/create-upvote', response_model=DocumentID)
def create_upvote(
        *,
        citizen_in: CitizenCreateVote,
        db: Database = Depends(get_db)
) -> Any:
    """ Create a new upvote
    """
    citizen_data = {'name': citizen_in.name,
                    'street_address': citizen_in.street_address,
                    'telephone_number': citizen_in.telephone_number}
    incident_id = citizen_in.incident

    # Check if the incident exists
    incident = db['incidents'].find_one({'_id': incident_id})
    if not incident:
        raise HTTPException(
            status_code=404,
            detail=f"Incident with id '{incident_id}' was not found",
            headers={'X-Error': 'Not Found Error'},
        )

    # Check if citizen's data exist in db
    citizen_db_data = db['citizens'].find_one(citizen_data)
    if citizen_db_data and citizen_db_data.get('_id', None) and incident.get('voted_by', None) \
            and citizen_db_data.get('_id') in incident.get('voted_by'):
        raise HTTPException(
            status_code=409,
            detail=f"You have already voted incident with id '{incident_id}'",
            headers={'X-Error': 'Double Submit'},
        )

    incident_ward = incident.get('ward', None)
    citizen_wards = citizen_db_data.get('wards', None) if citizen_db_data else None
    update_dict = {
        '$addToSet': {
            'voted_incidents': incident_id,
            'wards': incident_ward
        },
        '$inc': {
            'total_votes': 1,
            'total_wards': 1
        }
    }

    # If incident does not has ward or incident's ward already exists remove the update actions of the above dictionary
    if not incident_ward or (citizen_db_data and citizen_wards and incident_ward in citizen_wards):
        update_dict['$addToSet'].pop('wards')
        update_dict['$inc'].pop('total_wards')

    updated_citizen = db['citizens'].find_one_and_update(citizen_data, update_dict, upsert=True,
                                                         return_document=ReturnDocument.AFTER)

    # Update incident's voted_by field
    _ = db['incidents']. \
        update_one({'_id': incident_id},
                   {
                       '$addToSet': {
                           'voted_by': updated_citizen['_id']
                       },
                       '$inc': {
                           'total_votes': 1
                       }
                   }, upsert=False)

    return {'_id': updated_citizen['_id']}
