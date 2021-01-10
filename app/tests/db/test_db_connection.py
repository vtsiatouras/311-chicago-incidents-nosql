import pytest
from fastapi.testclient import TestClient
from pymongo import errors

from app.core.config import settings
from app.db.db_connection import get_db


def test_get_conn_(client: TestClient) -> None:
    db_connection = next(get_db())
    cur = db_connection['test_collection'].find({})
    assert list(cur) == []


def test_get_conn_fails_to_connect_with_wrong_user(client: TestClient) -> None:
    settings.MONGO_USER = 'FAKE_USER'
    settings.MONGO_PASSWORD = 'FAKE_PASSWORD'

    db_connection = next(get_db())
    cur = db_connection['test_collection'].find({})
    with pytest.raises(errors.OperationFailure):
        list(cur)


def test_get_conn_fails_to_connect_with_wrong_host(client: TestClient) -> None:

    settings.MONGO_HOST = 'FAKE_HOST'

    db_connection = next(get_db())
    cur = db_connection['test_collection'].find({})
    with pytest.raises(errors.ServerSelectionTimeoutError):
        list(cur)
