from typing import List
from faker import Faker

from app.db.db_connection import get_db
from app.models.models import Citizen


def fetch_random_incident_object_ids(number_of_incidents: int) -> List[str]:
    """ Fetches random ObjectIds

    :param number_of_incidents: Define the total of the unique incidents ids to fetch
    :return List of ObjectIds
    """
    db = next(get_db())
    incidents = set()
    while len(incidents) < number_of_incidents:
        incidents_cur = db['incidents'].aggregate([{"$sample": {"size": 100000}},
                                                   {"$project": {"_id": 1}}])
        for incident in incidents_cur:
            incidents.add(incident['_id'])

    return list(incidents)


def create_rng_citizens(number_of_citizens: int) -> List[dict]:
    fake = Faker()
    citizens = list()
    for it in range(number_of_citizens):
        citizen = {'name': fake.name(),
                   'street_address': fake.address(),
                   'telephone_number': fake.phone_number()}
        citizens.append(citizen)

    return citizens


def create_up_votes():
    """ Routine that casts citizen vote to random incidents in order to populate the database with up-votes data

    :return:
    """
    # incident_ids = fetch_random_incident_object_ids(number_of_incidents=2000000)
    citizens = create_rng_citizens(number_of_citizens=40000)
    print(citizens)


if __name__ == '__main__':
    create_up_votes()
