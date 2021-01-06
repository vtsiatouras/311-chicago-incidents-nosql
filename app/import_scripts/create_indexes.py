import pymongo

from app.db.db_connection import get_db


def create_indexes():
    db = next(get_db())
    # db['incidents'].create_index('type_of_service_request')
    db['incidents'].create_index([('creation_date', pymongo.ASCENDING)])


if __name__ == '__main__':
    create_indexes()
