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
    assert response == [{"_id": "ABANDONED_VEHICLE", "count": 6}, {"_id": "POTHOLE", "count": 3},
                        {"_id": "STREET_ONE_LIGHT", "count": 3}, {"_id": "GRAFFITI", "count": 2},
                        {"_id": "ALLEY_LIGHTS", "count": 1}]

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-type",
                   params={'start_date': '2019-04-09T00:00:00', 'end_date': '2020-04-09T00:00:00'})
    response = r.json()
    assert response == []


def test_total_requests_per_type_malformed_date_params(client: TestClient) -> None:
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

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-type", params={'start_date': '', 'end_date': ''})
    assert r.status_code == 422


def test_total_requests_per_type_start_date_greater_than_end_date(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/total-requests-per-type",
                   params={'start_date': '2017-04-09T00:00:00', 'end_date': '2014-04-09T00:00:00'})
    assert r.status_code == 422


def test_total_requests_per_day(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '2014-04-09T00:00:00', 'end_date': '2017-04-09T00:00:00',
                           'request_type': 'ABANDONED_VEHICLE'})
    response = r.json()
    assert response == [{"_id": "2015-05-08T00:00:00", "count": 2},
                        {"_id": "2015-04-08T00:00:00", "count": 2},
                        {"_id": "2015-04-07T00:00:00", "count": 2}]

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '2019-04-09T00:00:00', 'end_date': '2020-04-09T00:00:00',
                           'request_type': 'ABANDONED_VEHICLE'})

    response = r.json()
    assert response == []

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '2014-04-09T00:00:00', 'end_date': '2017-04-09T00:00:00',
                           'request_type': 'RODENT_BAITING'})
    response = r.json()
    assert response == []

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '2014-04-09T00:00:00', 'end_date': '2017-04-09T00:00:00',
                           'request_type': 'GRAFFITI'})
    response = r.json()
    assert response == [{"_id": "2015-05-08T00:00:00", "count": 2}]


def test_total_requests_per_day_malformed_date_params(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '00:00:00', 'end_date': '2017-04-09T00:00:00', 'request_type': 'GRAFFITI'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '2017-04-09T00:00:00', 'end_date': '00:00:00', 'request_type': 'GRAFFITI'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '', 'end_date': '2017-04-09T00:00:00', 'request_type': 'GRAFFITI'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '2017-04-09T00:00:00', 'end_date': '', 'request_type': 'GRAFFITI'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '', 'end_date': '',
                           'request_type': 'GRAFFITI'})
    assert r.status_code == 422


def test_total_requests_per_day_start_date_greater_than_end_date(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '2017-04-09T00:00:00', 'end_date': '2014-04-09T00:00:00',
                           'request_type': 'GRAFFITI'})
    assert r.status_code == 422


def test_total_requests_per_request_type_param(client: TestClient) -> None:
    param_types = ['ABANDONED_VEHICLE', 'ALLEY_LIGHTS', 'GRAFFITI', 'GARBAGE', 'POTHOLE', 'RODENT_BAITING',
                   'SANITATION_VIOLATION', 'STREET_ONE_LIGHT', 'STREET_ALL_LIGHTS', 'TREE_TRIM', 'TREE_DEBRIS']
    for param in param_types:
        r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                       params={'start_date': '2013-04-09T00:00:00', 'end_date': '2014-04-09T00:00:00',
                               'request_type': param})
        assert r.status_code == 200


def test_total_requests_per_request_malformed_type_param(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '2013-04-09T00:00:00', 'end_date': '2014-04-09T00:00:00',
                           'request_type': 'ASDF'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/total-requests-per-day",
                   params={'start_date': '2013-04-09T00:00:00', 'end_date': '2014-04-09T00:00:00',
                           'request_type': ''})
    assert r.status_code == 422


def test_three_most_common_requests_per_zipcode(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/three-most-common-requests-per-zipcode",
                   params={'date': '2015-05-08T00:00:00'})
    response = r.json()
    assert len(response) == 4
    r = client.get(f"{settings.API_V1_STR}/three-most-common-requests-per-zipcode",
                   params={'date': '2020-05-08T00:00:00'})
    response = r.json()
    assert len(response) == 0


def test_three_most_common_requests_per_zipcode_malformed_date_param(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/three-most-common-requests-per-zipcode",
                   params={'date': '00:00:00'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/three-most-common-requests-per-zipcode",
                   params={'start_date': ''})
    assert r.status_code == 422


def test_three_least_common_wards(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/three-least-common-wards",
                   params={'request_type': 'ABANDONED_VEHICLE'})
    response = r.json()
    assert response == [{'_id': 45, 'count': 1}, {'_id': 43, 'count': 2}, {'_id': 44, 'count': 3}]

    # There is a record with type of request STREET_ONE_LIGHT which does not have ward.
    # The total requests with type STREET_ONE_LIGHT are 3
    r = client.get(f"{settings.API_V1_STR}/three-least-common-wards",
                   params={'request_type': 'STREET_ONE_LIGHT'})
    response = r.json()
    assert response == [{'_id': 45, 'count': 2}]

    r = client.get(f"{settings.API_V1_STR}/three-least-common-wards",
                   params={'request_type': 'STREET_ALL_LIGHTS'})
    response = r.json()
    assert response == []


def test_three_least_common_wards_malformed_type_param(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/three-least-common-wards",
                   params={'request_type': 'ASDF'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/three-least-common-wards",
                   params={'request_type': ''})
    assert r.status_code == 422
