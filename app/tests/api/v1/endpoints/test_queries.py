from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.db_connection import get_db
from app.main import app
from ....conftest import override_db_conn_with_data

app.dependency_overrides[get_db] = override_db_conn_with_data


def test_total_requests_per_type(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/total-requests-per-type",
                   params={'start_date': '2014-04-09T00:00:00', 'end_date': '2017-04-09T00:00:00'})
    response = r.json()
    assert response == [{"_id": "Abandoned Vehicle Complaint", "count": "3"},
                        {"_id": "Pothole in Street", "count": "3"}, {"_id": "Street Light Out", "count": "3"},
                        {"_id": "Graffiti Removal", "count": "2"}, {"_id": "Alley Light Put", "count": "1"}]

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-type",
                   params={'start_date': '2019-04-09T00:00:00', 'end_date': '2020-04-09T00:00:00'})
    response = r.json()
    assert response == []


def test_total_requests_per_type_malformed_params(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/total-requests-per-type",
                   params={'start_date': '00:00:00', 'end_date': '2017-04-09T00:00:00'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-type",
                   params={'start_date': '2017-04-09T00:00:00', 'end_date': '00:00:00'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-type",
                   params={'start_date': '', 'end_date': '2017-04-09T00:00:00'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-type",
                   params={'start_date': '2017-04-09T00:00:00', 'end_date': ''})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-type",
                   params={'start_date': '2017-04-09T00:00:00', 'end_date': '2014-04-09T00:00:00'})
    assert r.status_code == 422
