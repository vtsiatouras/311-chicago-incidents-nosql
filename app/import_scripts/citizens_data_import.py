import random

from typing import List, Tuple
from faker import Faker

from app.db.db_connection import get_db


NUMBER_OF_CITIZENS = 80000
MAX_VOTES_PER_CITIZEN = 1000


def fetch_random_incident_object_ids(number_of_incidents: int) -> Tuple[List[str], dict]:
    """ Fetches random ObjectIds

    :param number_of_incidents: Define the total of the unique incidents ids to fetch
    :return List of ObjectIds and a dictionary with ObjectIds wards pairs
    """
    db = next(get_db())
    incidents = set()
    object_ids_with_wards = dict()
    while len(incidents) < number_of_incidents:
        incidents_cur = db['incidents'].aggregate([{'$sample': {'size': 50000}},
                                                   {'$project': {'_id': 1, 'ward': 1}}])
        for incident in incidents_cur:
            object_ids_with_wards.update({incident.get('_id'): incident.get('ward')})
            incidents.add(incident.get('_id'))

    return list(incidents), object_ids_with_wards


def create_rng_citizens(number_of_citizens: int) -> List[dict]:
    """ Method that generate citizen data

    :param number_of_citizens: The amount of citizens to generate
    :return: List that contains the generated citizen data
    """
    fake = Faker()
    citizens = list()
    for it in range(number_of_citizens):
        citizen = {'name': fake.name(),
                   'street_address': fake.address(),
                   'telephone_number': fake.phone_number()}
        citizens.append(citizen)

    return citizens


def list_random_chunks(elements_list: list, number_of_chunks: int, max_size: int = MAX_VOTES_PER_CITIZEN) -> List:
    """ Method that initially shuffles the elements of a list and splits it into random sized chunks

    :param elements_list: The list to split
    :param number_of_chunks: The total number of chunks
    :param max_size: The max size of a chunk
    :return: A list that contains random sized chunks
    """
    chunks = [set() for _ in range(number_of_chunks)]

    # Generate the max sizes of each chunk
    chunks_sizes = list()
    for i in range(number_of_chunks):
        chunks_sizes.append(random.randint(1, max_size))

    random.shuffle(elements_list)

    # Assign all elements of the list at least one time to the chunks
    for it, element in enumerate(elements_list):
        chunks[it % number_of_chunks].add(element)

    # Fill up chunks based on the random sizes that generated above
    it = 0
    for chunk in chunks:
        chunk_size = chunks_sizes[it]
        while len(chunk) < chunk_size:
            chunk.add(elements_list[random.randint(1, len(elements_list) - 1)])
        it += 1

    return chunks


def create_up_votes() -> None:
    """ Routine that casts citizen vote to random incidents in order to populate the database with up-votes data

    :return: None
    """
    incident_ids, object_ids_with_wards = fetch_random_incident_object_ids(number_of_incidents=2000000)
    citizens = create_rng_citizens(number_of_citizens=NUMBER_OF_CITIZENS)
    votes_list = list_random_chunks(elements_list=incident_ids, number_of_chunks=NUMBER_OF_CITIZENS)

    # Assign votes to citizens
    it = 0
    for citizen in citizens:

        wards = set()
        for vote in votes_list[it]:
            ward = object_ids_with_wards.get(vote)
            if ward:
                wards.add(ward)

        citizen.update({'voted_incidents': list(votes_list[it])})
        citizen.update({'total_votes': len(votes_list[it])})
        citizen.update({'wards': list(wards)})
        citizen.update({'total_wards': len(wards)})

        it += 1

    db = next(get_db())
    db['citizens'].insert_many(citizens)

    # Fetch citizen data
    citizens_docs = db['citizens'].find({})

    # Create a dictionary that associates Incident ObjectIds with Citizen ObjectIds
    votes_per_incident = dict()
    for citizen_doc in citizens_docs:
        voted_incidents = citizen_doc['voted_incidents']
        for voted_incident in voted_incidents:
            try:
                votes_per_incident[voted_incident].append(citizen_doc['_id'])
            except KeyError:
                votes_per_incident[voted_incident] = [citizen_doc['_id']]

    # Assign votes to incidents
    for incident_id, citizens_ids in votes_per_incident.items():
        db['incidents'].update_many(
            {'_id': incident_id},
            {
                '$set': {
                    'total_votes': len(citizens_ids),
                    'voted_by': citizens_ids
                }
            },
            upsert=False
        )
