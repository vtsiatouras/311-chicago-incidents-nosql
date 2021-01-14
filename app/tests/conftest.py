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


mock_client = mongomock.MongoClient()
mock_db_empty = mock_client['incidents_test_db_empty']
mock_db_loaded = mock_client['incidents_test_db_loaded']


@pytest.fixture()
def db_empty_fixture():
    mock_db_empty.drop_collection('incidents')
    mock_db_empty.drop_collection('citizens')


@pytest.fixture(scope='function', autouse=True)
def db_loaded_fixture():
    mock_db_loaded['incidents'].insert_many(mock_incident_docs)
    mock_db_loaded['citizens'].insert_many(mock_citizen_docs)
    yield mock_db_loaded
    mock_db_loaded.drop_collection('incidents')
    mock_db_loaded.drop_collection('citizens')


def override_db_conn_static_empty():
    return mock_db_empty


def override_db_conn_with_data():
    return mock_db_loaded
