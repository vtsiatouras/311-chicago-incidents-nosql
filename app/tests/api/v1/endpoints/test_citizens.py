from bson import ObjectId
from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.db_connection import get_db
from app.main import app
from ....conftest import override_db_conn_static_empty, override_db_conn_with_data, mock_db_loaded


def test_create_upvote_new_citizen_simple(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    # New citizen
    citizen_data = {
        "name": "Test User",
        "street_address": "Test Address",
        "telephone_number": "123 456 7890",
        "incident": "5ffdf75c0d58d021a3abaf71"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    # Returns citizen's id
    response = r.json()
    assert r.status_code == 200

    obj = mock_db_loaded['citizens'].find_one({'_id': ObjectId(response['_id'])})
    assert obj['voted_incidents'] == [ObjectId('5ffdf75c0d58d021a3abaf71')]
    assert obj['total_votes'] == 1
    assert obj['wards'] == [44]
    assert obj['total_wards'] == 1

    obj = mock_db_loaded['incidents'].find_one({'_id': ObjectId('5ffdf75c0d58d021a3abaf71')})
    assert ObjectId(response['_id']) in obj['voted_by']


def test_create_upvote_new_citizen_duplicate(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    # New citizen
    citizen_data = {
        "name": "Test User",
        "street_address": "Test Address",
        "telephone_number": "123 456 7890",
        "incident": "5ffdf75c0d58d021a3abaf71"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    assert r.status_code == 200

    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    assert r.status_code == 409


def test_create_upvote_existing_user(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    # Existing citizen
    citizen_data = {
        "name": "Alexander Rose",
        "street_address": "638 Angela Burg Suite 215\nSouth Aaronbury,",
        "telephone_number": "123456789",
        "incident": "5ffdf6fe0d58d021a39b2f10"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    assert r.status_code == 200

    # Ensure that we didn't create new citizen
    obj = mock_db_loaded['citizens'].find({'name': 'Alexander Rose'})
    result = list(obj)
    assert len(result) == 1

    obj = mock_db_loaded['incidents'].find_one({'_id': ObjectId('5ffdf6fe0d58d021a39b2f10')})
    assert ObjectId(result[0]['_id']) in obj['voted_by']


def test_create_upvote_existing_user_duplicate(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    # Existing citizen
    citizen_data = {
        "name": "Alexander Rose",
        "street_address": "638 Angela Burg Suite 215\nSouth Aaronbury,",
        "telephone_number": "123456789",
        "incident": "5ffdf75c0d58d021a3abaf71"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    assert r.status_code == 409


def test_create_upvote_with_incident_without_ward_new_citizen(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    # New citizen
    citizen_data = {
        "name": "Test User",
        "street_address": "Test Address",
        "telephone_number": "123 456 7890",
        "incident": "5ffdf8750d58d021a3b43220"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    response = r.json()
    assert r.status_code == 200

    obj = mock_db_loaded['citizens'].find_one({'_id': ObjectId(response['_id'])})
    assert obj['voted_incidents'] == [ObjectId('5ffdf8750d58d021a3b43220')]
    assert obj['total_votes'] == 1
    assert 'wards' not in obj
    assert 'total_wards' not in obj

    obj = mock_db_loaded['incidents'].find_one({'_id': ObjectId('5ffdf8750d58d021a3b43220')})
    assert ObjectId(response['_id']) in obj['voted_by']


def test_create_upvote_with_incident_without_ward_existing_citizen(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    # Existing citizen
    citizen_data = {
        "name": "Alexander Rose",
        "street_address": "638 Angela Burg Suite 215\nSouth Aaronbury,",
        "telephone_number": "123456789",
        "incident": "5ffdf8750d58d021a3b43220"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    response = r.json()
    assert r.status_code == 200

    obj = mock_db_loaded['citizens'].find_one({'_id': ObjectId(response['_id'])})
    assert obj['voted_incidents'] == [ObjectId("5ffdf75c0d58d021a3abaf71"), ObjectId("5ffdf65f0d58d021a394a8ef"),
                                      ObjectId("5ffdf6fe0d58d021a39b2f6a"), ObjectId("5ffdf8750d58d021a3b43220")]
    assert obj['total_votes'] == 4
    # No new ward added
    assert obj['wards'] == [44, 45]
    assert obj['total_wards'] == 2

    obj = mock_db_loaded['incidents'].find_one({'_id': ObjectId('5ffdf8750d58d021a3b43220')})
    assert ObjectId(response['_id']) in obj['voted_by']


def test_create_upvote_multiple_upvotes_from_many_users(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    # New citizen
    citizen_data = {
        "name": "Test User",
        "street_address": "Test Address",
        "telephone_number": "123 456 7890",
        "incident": "5ffdf8750d58d021a3b43220"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    # Returns citizen's id
    response_1 = r.json()
    assert r.status_code == 200

    # Existing citizen
    citizen_data = {
        "name": "Alexander Rose",
        "street_address": "638 Angela Burg Suite 215\nSouth Aaronbury,",
        "telephone_number": "123456789",
        "incident": "5ffdf8750d58d021a3b43220"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    response_2 = r.json()
    assert r.status_code == 200

    obj = mock_db_loaded['incidents'].find_one({'_id': ObjectId('5ffdf8750d58d021a3b43220')})
    assert ObjectId(response_1['_id']) in obj['voted_by']
    assert ObjectId(response_2['_id']) in obj['voted_by']
    assert obj['total_votes'] == 2


def test_create_upvote_multiple_upvotes_from_one_user(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    # New citizen
    citizen_data = {
        "name": "Test User",
        "street_address": "Test Address",
        "telephone_number": "123 456 7890",
        "incident": "5ffdf8750d58d021a3b43220"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    # Returns citizen's id
    response = r.json()
    assert r.status_code == 200

    citizen_data = {
        "name": "Test User",
        "street_address": "Test Address",
        "telephone_number": "123 456 7890",
        "incident": "5ffdf8750d58d021a3b43221"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    # Returns citizen's id
    response = r.json()
    assert r.status_code == 200

    obj = mock_db_loaded['incidents'].find_one({'_id': ObjectId('5ffdf8750d58d021a3b43220')})
    assert ObjectId(response['_id']) in obj['voted_by']
    assert obj['total_votes'] == 1

    obj = mock_db_loaded['incidents'].find_one({'_id': ObjectId('5ffdf8750d58d021a3b43221')})
    assert ObjectId(response['_id']) in obj['voted_by']
    assert obj['total_votes'] == 1

    obj = mock_db_loaded['citizens'].find_one({'_id': ObjectId(response['_id'])})
    assert obj['total_votes'] == 2


def test_create_upvote_with_unknown_incident(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    # Existing citizen
    citizen_data = {
        "name": "Alexander Rose",
        "street_address": "638 Angela Burg Suite 215\nSouth Aaronbury,",
        "telephone_number": "123456789",
        "incident": "000df8750d58d021a3b43220"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    assert r.status_code == 404


def test_create_upvote_malformed_incident_id(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    # Existing citizen
    citizen_data = {
        "name": "Alexander Rose",
        "street_address": "638 Angela Burg Suite 215\nSouth Aaronbury,",
        "telephone_number": "123456789",
        "incident": "000dasdsadasdf8750d58d021a3b43220"
    }
    r = client.post(f"{settings.API_V1_STR}/create-upvote", json=citizen_data)
    assert r.status_code == 422
