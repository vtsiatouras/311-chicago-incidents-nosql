from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.db_connection import get_db
from app.main import app
from ....conftest import override_db_conn_static_empty, override_db_conn_with_data


def test_create_get_incident_integration(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_static_empty
    incident = {
        "creation_date": "2021-01-14T00:42:56.763Z",
        "completion_date": "2021-01-14T00:42:56.763Z",
        "status": "OPEN",
        "service_request_number": "123",
        "type_of_service_request": "STREET_ONE_LIGHT",
        "current_activity": "Doing something",
        "most_recent_action": "Reported",
        "street_address": "123 Test Street",
        "zip_code": 12345,
        "ward": 1,
        "historical_wards_03_15": 10,
        "police_district": 1,
        "community_area": 1,
        "community_areas": 1,
        "ssa": 1,
        "census_tracts": 1,
        "latitude": 43.3123131,
        "longitude": -60.4324234
    }
    r = client.post(f"{settings.API_V1_STR}/create-incident", json=incident)
    response = r.json()
    assert r.status_code == 200

    r = client.get(f"{settings.API_V1_STR}/get-incident", params={'incident_id': response['_id']})
    incident_from_db = r.json()
    assert r.status_code == 200
    assert incident_from_db['service_request_number'] == incident['service_request_number']


def test_create_incident_missing_creation_date(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_static_empty
    incident = {
        "completion_date": "2021-01-14T00:42:56.763Z",
        "status": "OPEN",
        "service_request_number": "123",
        "type_of_service_request": "STREET_ONE_LIGHT",
        "current_activity": "Doing something",
        "most_recent_action": "Reported",
        "street_address": "123 Test Street",
        "zip_code": 12345,
        "ward": 1,
        "historical_wards_03_15": 10,
        "police_district": 1,
        "community_area": 1,
        "community_areas": 1,
        "ssa": 1,
        "census_tracts": 1,
        "latitude": 43.3123131,
        "longitude": -60.4324234
    }
    r = client.post(f"{settings.API_V1_STR}/create-incident", json=incident)
    assert r.status_code == 422


def test_create_incident_missing_status(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_static_empty
    incident = {
        "creation_date": "2021-01-14T00:42:56.763Z",
        "completion_date": "2021-01-14T00:42:56.763Z",
        "service_request_number": "123",
        "type_of_service_request": "STREET_ONE_LIGHT",
        "current_activity": "Doing something",
        "most_recent_action": "Reported",
        "street_address": "123 Test Street",
        "zip_code": 12345,
        "ward": 1,
        "historical_wards_03_15": 10,
        "police_district": 1,
        "community_area": 1,
        "community_areas": 1,
        "ssa": 1,
        "census_tracts": 1,
        "latitude": 43.3123131,
        "longitude": -60.4324234
    }
    r = client.post(f"{settings.API_V1_STR}/create-incident", json=incident)
    assert r.status_code == 422


def test_create_incident_missing_service_request_number(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_static_empty
    incident = {
        "creation_date": "2021-01-14T00:42:56.763Z",
        "completion_date": "2021-01-14T00:42:56.763Z",
        "status": "OPEN",
        "type_of_service_request": "STREET_ONE_LIGHT",
        "current_activity": "Doing something",
        "most_recent_action": "Reported",
        "street_address": "123 Test Street",
        "zip_code": 12345,
        "ward": 1,
        "historical_wards_03_15": 10,
        "police_district": 1,
        "community_area": 1,
        "community_areas": 1,
        "ssa": 1,
        "census_tracts": 1,
        "latitude": 43.3123131,
        "longitude": -60.4324234
    }
    r = client.post(f"{settings.API_V1_STR}/create-incident", json=incident)
    assert r.status_code == 422


def test_create_incident_missing_type_of_service_request(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_static_empty
    incident = {
        "creation_date": "2021-01-14T00:42:56.763Z",
        "completion_date": "2021-01-14T00:42:56.763Z",
        "status": "OPEN",
        "service_request_number": "123",
        "current_activity": "Doing something",
        "most_recent_action": "Reported",
        "street_address": "123 Test Street",
        "zip_code": 12345,
        "ward": 1,
        "historical_wards_03_15": 10,
        "police_district": 1,
        "community_area": 1,
        "community_areas": 1,
        "ssa": 1,
        "census_tracts": 1,
        "latitude": 43.3123131,
        "longitude": -60.4324234
    }
    r = client.post(f"{settings.API_V1_STR}/create-incident", json=incident)
    assert r.status_code == 422


def test_create_incident_missing_street_address(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_static_empty
    incident = {
        "creation_date": "2021-01-14T00:42:56.763Z",
        "completion_date": "2021-01-14T00:42:56.763Z",
        "status": "OPEN",
        "service_request_number": "123",
        "type_of_service_request": "STREET_ONE_LIGHT",
        "current_activity": "Doing something",
        "most_recent_action": "Reported",
        "zip_code": 12345,
        "ward": 1,
        "historical_wards_03_15": 10,
        "police_district": 1,
        "community_area": 1,
        "community_areas": 1,
        "ssa": 1,
        "census_tracts": 1,
        "latitude": 43.3123131,
        "longitude": -60.4324234
    }
    r = client.post(f"{settings.API_V1_STR}/create-incident", json=incident)
    assert r.status_code == 422


def test_get_incident(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    r = client.get(f"{settings.API_V1_STR}/get-incident", params={'incident_id': '5ffdf6fe0d58d021a39b2f6a'})
    incident_from_db = r.json()
    assert r.status_code == 200
    assert incident_from_db['service_request_number'] == '15-01207495'


def test_get_incident_not_found(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    r = client.get(f"{settings.API_V1_STR}/get-incident", params={'incident_id': '333df6fe0d58d021a39b2f6a'})
    assert r.status_code == 404


def test_get_incident_malformed_incident_id(client: TestClient) -> None:
    app.dependency_overrides[get_db] = override_db_conn_with_data
    r = client.get(f"{settings.API_V1_STR}/get-incident", params={'incident_id': '5ffdf6fe0d58d021a39b2f6a11111'})
    assert r.status_code == 422
