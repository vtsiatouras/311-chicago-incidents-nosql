import mongomock
import pytest

from typing import Generator
from fastapi.testclient import TestClient

from app.main import app
from .test_data import mock_incident_docs, mock_citizen_docs


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


def override_db_conn_empty():
    mock_client = mongomock.MongoClient()
    mock_db = mock_client['incidents_test_db']
    return mock_db


def override_db_conn_with_data():
    mock_client = mongomock.MongoClient()
    mock_db = mock_client['incidents_test_db']
    mock_db['incidents'].insert_many(mock_incident_docs)
    mock_db['citizens'].insert_many(mock_citizen_docs)
    return mock_db
