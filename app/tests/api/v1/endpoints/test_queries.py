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
    assert response == [{'_id': 'ABANDONED_VEHICLE', 'count': 6}, {'_id': 'POTHOLE', 'count': 3},
                        {'_id': 'STREET_ONE_LIGHT', 'count': 3}, {'_id': 'GRAFFITI', 'count': 2},
                        {'_id': 'ALLEY_LIGHTS', 'count': 1}]

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
    assert response == [{'_id': '2015-05-08T00:00:00', 'count': 2},
                        {'_id': '2015-04-08T00:00:00', 'count': 2},
                        {'_id': '2015-04-07T00:00:00', 'count': 2}]

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
                   params={'date': ''})
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
    assert response == [{'_id': 45, 'count': 1}, {'_id': 46, 'count': 1}]

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


def test_average_completion_time_per_request(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/average-completion-time-per-request",
                   params={'start_date': '2014-04-09T00:00:00', 'end_date': '2017-04-09T00:00:00'})
    response = r.json()
    assert response == [{'_id': 'ABANDONED_VEHICLE', 'average_completion_time': '11 days, 16:00:00'},
                        {'_id': 'ALLEY_LIGHTS', 'average_completion_time': '32 days, 0:00:00'},
                        {'_id': 'GRAFFITI', 'average_completion_time': '32 days, 0:00:00'},
                        {'_id': 'POTHOLE', 'average_completion_time': '32 days, 0:00:00'},
                        {'_id': 'STREET_ONE_LIGHT', 'average_completion_time': '32 days, 0:00:00'}]

    r = client.get(f"{settings.API_V1_STR}/average-completion-time-per-request",
                   params={'start_date': '2019-04-09T00:00:00', 'end_date': '2020-04-09T00:00:00'})
    response = r.json()
    assert response == []


def test_average_completion_time_per_request_malformed_date_params(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/average-completion-time-per-request",
                   params={'start_date': '00:00:00', 'end_date': '2017-04-09T00:00:00'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/average-completion-time-per-request",
                   params={'start_date': '2017-04-09T00:00:00', 'end_date': '00:00:00'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/average-completion-time-per-request",
                   params={'start_date': '', 'end_date': '2017-04-09T00:00:00'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/average-completion-time-per-request",
                   params={'start_date': '2017-04-09T00:00:00', 'end_date': ''})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/average-completion-time-per-request",
                   params={'start_date': '', 'end_date': ''})
    assert r.status_code == 422


def test_most_common_service_in_bounding_box(client: TestClient) -> None:
    # NotImplementedError: '$geoWithin' is a valid operation but it is not supported by Mongomock yet. :(
    # r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
    #                params={'date': '2015-04-09T00:00:00',
    #                        'point_a_longitude': -88.64615132728282,
    #                        'point_a_latitude': 40.93702589972641,
    #                        'point_b_longitude': -80.64615132728282,
    #                        'point_b_latitude': 49.93702589972641})
    # response = r.json()
    # assert response == [{'_id': 'ABANDONED_VEHICLE', 'count': 5}]

    # r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
    #                params={'start_date': '2019-04-09T00:00:00', 'end_date': '2020-04-09T00:00:00'})
    # response = r.json()
    # assert response == []
    assert True


def test_most_common_service_in_bounding_box_malformed_coordinate_params(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
                   params={'date': '2015-04-09T00:00:00asdf',
                           'point_a_longitude': -88.64615132728282,
                           'point_a_latitude': 40.93702589972641,
                           'point_b_longitude': -80.64615132728282,
                           'point_b_latitude': 49.93702589972641})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
                   params={'date': '2015-04-09T00:00:00',
                           'point_a_longitude': '-88.64615132728282asdf',
                           'point_a_latitude': 40.93702589972641,
                           'point_b_longitude': -80.64615132728282,
                           'point_b_latitude': 49.93702589972641})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
                   params={'point_a_longitude': -88.64615132728282,
                           'point_a_latitude': 'asd40.93702589972641',
                           'point_b_longitude': -80.64615132728282,
                           'point_b_latitude': 49.93702589972641})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
                   params={'point_a_longitude': -88.64615132728282,
                           'point_a_latitude': 40.93702589972641,
                           'point_b_longitude': 'asd-80.64615132728282',
                           'point_b_latitude': 49.93702589972641})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
                   params={'point_a_longitude': -88.64615132728282,
                           'point_a_latitude': 40.93702589972641,
                           'point_b_longitude': -80.64615132728282,
                           'point_b_latitude': 'asd49.93702589972641'})
    assert r.status_code == 422


def test_most_common_service_in_bounding_box_missing_coordinate_params(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
                   params={'date': '',
                           'point_a_longitude': 80.64615132728282,
                           'point_a_latitude': 40.93702589972641,
                           'point_b_longitude': 80.64615132728282,
                           'point_b_latitude': 49.93702589972641})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
                   params={'point_a_longitude': '',
                           'point_a_latitude': 40.93702589972641,
                           'point_b_longitude': 80.64615132728282,
                           'point_b_latitude': 49.93702589972641})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
                   params={'point_a_longitude': -88.64615132728282,
                           'point_a_latitude': '',
                           'point_b_longitude': 80.64615132728282,
                           'point_b_latitude': 49.93702589972641})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
                   params={'point_a_longitude': -88.64615132728282,
                           'point_a_latitude': 80.64615132728282,
                           'point_b_longitude': '',
                           'point_b_latitude': 49.93702589972641})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/most-common-service-in-bounding-box",
                   params={'point_a_longitude': -88.64615132728282,
                           'point_a_latitude': 80.64615132728282,
                           'point_b_longitude': 49.93702589972641,
                           'point_b_latitude': ''})
    assert r.status_code == 422


def test_top_fifty_upvoted_requests(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/top-fifty-upvoted-requests",
                   params={'date': '2015-05-08T00:00:00'})
    response = r.json()
    assert response == [{'_id': '5ffdf8750d58d021a3b43219', 'total_votes': 9},
                        {'_id': '5ffdf8750d58d021a3b43218', 'total_votes': 8},
                        {'_id': '5ffdf8750d58d021a3b43217', 'total_votes': 7},
                        {'_id': '5ffdf8750d58d021a3b43216', 'total_votes': 6},
                        {'_id': '5ffdf8750d58d021a3b43214', 'total_votes': 5},
                        {'_id': '5ffdf8750d58d021a3b43213', 'total_votes': 4},
                        {'_id': '5ffdf8750d58d021a3b43211', 'total_votes': 3},
                        {'_id': '5ffdf8750d58d021a3b43215', 'total_votes': 2},
                        {'_id': '5ffdf8750d58d021a3b43212', 'total_votes': 1},
                        {'_id': '5ffdf8750d58d021a3b43220', 'total_votes': None},
                        {'_id': '5ffdf8750d58d021a3b43221', 'total_votes': None}]

    r = client.get(f"{settings.API_V1_STR}/top-fifty-upvoted-requests",
                   params={'date': '2020-05-08T00:00:00'})
    response = r.json()

    assert response == []


def test_top_fifty_upvoted_requests_malformed_date_param(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/top-fifty-upvoted-requests",
                   params={'date': '00:00:00'})
    assert r.status_code == 422

    r = client.get(f"{settings.API_V1_STR}/top-fifty-upvoted-requests",
                   params={'date': ''})
    assert r.status_code == 422


def test_top_fifty_active_citizens(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/top-fifty-active-citizens")
    response = r.json()
    assert response == [{'_id': '5ffdf8750d58d021a3b432e8', 'total_votes': 9},
                        {'_id': '5ffdf8750d58d021a3b432e9', 'total_votes': 4},
                        {'_id': '5ffdf8750d58d021a3b432e7', 'total_votes': 3}]


def test_top_fifty_wards_citizens(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/top-fifty-wards-citizens")
    response = r.json()
    assert response == [{'_id': '5ffdf8750d58d021a3b432e8', 'total_wards': 5},
                        {'_id': '5ffdf8750d58d021a3b432e9', 'total_wards': 4},
                        {'_id': '5ffdf8750d58d021a3b432e7', 'total_wards': 2}]


def test_phone_number_incidents(client: TestClient) -> None:
    # NotImplementedError: Although '$reduce' is a valid array operator for the aggregation pipeline, it is currently
    # not implemented in Mongomock.
    # r = client.get(f"{settings.API_V1_STR}/phone-number-incidents")
    # response = r.json()
    # assert response == []
    assert True
