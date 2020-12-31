from pymongo import MongoClient

from app.core.config import settings


def get_db():
    db_client = MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT, username=settings.MONGO_USER,
                            password=settings.MONGO_PASSWORD, authSource=settings.MONGO_DB)
    db_conn = db_client[settings.MONGO_DB]
    yield db_conn
