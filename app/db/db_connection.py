from pymongo import MongoClient

from app.core.config import settings


client = MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT, username=settings.MONGO_USER,
                     password=settings.MONGO_PASSWORD, authSource=settings.MONGO_DB)
db = client[settings.MONGO_DB]
