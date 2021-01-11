import pandas as pd
import numpy as np

from app.db.db_connection import get_db


def import_abandoned_vehicles(input_file: str) -> None:
    """ Import the requests for abandoned vehicles to the database.

    :param input_file: The file from which to load the requests for abandoned vehicles.
    """
    print("Getting requests for abandoned vehicles")
    db = next(get_db())

    input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})
    input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                        'type_of_service_request', 'license_plate', 'vehicle_make_model', 'vehicle_color',
                        'current_activity', 'most_recent_action', 'days_of_report_as_parked', 'street_address',
                        'zip_code', 'x_coordinate', 'y_coordinate', 'ward', 'police_district', 'community_area',
                        'ssa', 'latitude', 'longitude', 'geo_location', 'historical_wards_03_15', 'zip_codes',
                        'community_areas', 'census_tracts', 'wards']
    input_df = __dataframe_normalization__(input_df, 'ABANDONED_VEHICLE')
    df_docs = input_df.to_dict(orient='records')
    docs = []
    for df_doc in df_docs:
        docs.append({k: v for k, v in df_doc.items() if v is not None})
    db['incidents'].insert_many(docs)


def import_garbage_carts(input_file: str) -> None:
    """ Import the requests for garbage carts to the database.

    :param input_file: The file from which to load the requests for garbage carts.
    """
    print("Getting requests for garbage carts")
    db = next(get_db())

    input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})

    input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                        'type_of_service_request', 'number_of_elements', 'current_activity',
                        'most_recent_action', 'street_address', 'zip_code', 'x_coordinate', 'y_coordinate',
                        'ward', 'police_district', 'community_area', 'ssa', 'latitude', 'longitude',
                        'geo_location', 'historical_wards_03_15', 'zip_codes', 'community_areas',
                        'census_tracts', 'wards']
    input_df = __dataframe_normalization__(input_df, 'GARBAGE_CART')
    df_docs = input_df.to_dict(orient='records')
    docs = []
    for df_doc in df_docs:
        docs.append({k: v for k, v in df_doc.items() if v is not None})
    db['incidents'].insert_many(docs)


def import_potholes(input_file: str) -> None:
    """ Import the requests for potholes to the database.

    :param input_file: The file from which to load the requests for potholes.
    """
    print("Getting requests for potholes")
    db = next(get_db())

    input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})

    input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                        'type_of_service_request', 'current_activity', 'most_recent_action',
                        'number_of_elements', 'street_address', 'zip_code', 'x_coordinate', 'y_coordinate',
                        'ward', 'police_district', 'community_area', 'ssa', 'latitude', 'longitude',
                        'geo_location', 'historical_wards_03_15', 'zip_codes', 'community_areas',
                        'census_tracts', 'wards']
    input_df = __dataframe_normalization__(input_df, 'POTHOLE')
    df_docs = input_df.to_dict(orient='records')
    docs = []
    for df_doc in df_docs:
        docs.append({k: v for k, v in df_doc.items() if v is not None})
    db['incidents'].insert_many(docs)


def import_graffiti(input_file: str) -> None:
    """ Import the requests for graffiti to the database.

    :param input_file: The file from which to load the requests for graffiti.
    """
    print("Getting requests for graffiti")
    db = next(get_db())

    input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})

    input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                        'type_of_service_request', 'surface', 'graffiti_location', 'street_address',
                        'zip_code', 'x_coordinate', 'y_coordinate', 'ward', 'police_district', 'community_area',
                        'ssa', 'latitude', 'longitude', 'geo_location', 'historical_wards_03_15', 'zip_codes',
                        'community_areas', 'census_tracts', 'wards']
    input_df = __dataframe_normalization__(input_df, 'GRAFFITI')
    df_docs = input_df.to_dict(orient='records')
    docs = []
    for df_doc in df_docs:
        docs.append({k: v for k, v in df_doc.items() if v is not None})
    db['incidents'].insert_many(docs)


def import_rodent_baiting(input_file: str) -> None:
    """ Import the requests for rodent baiting to the database.

    :param input_file: The file from which to load the requests for rodent baiting.
    """
    print("Getting requests for rodent baiting")
    db = next(get_db())

    input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})

    input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                        'type_of_service_request', 'number_of_premises_baited', 'number_of_premises_w_garbage',
                        'number_of_premises_w_rats', 'current_activity', 'most_recent_action', 'street_address',
                        'zip_code', 'x_coordinate', 'y_coordinate', 'ward', 'police_district', 'community_area',
                        'latitude', 'longitude', 'geo_location', 'historical_wards_03_15', 'zip_codes',
                        'community_areas', 'census_tracts', 'wards']
    input_df = __dataframe_normalization__(input_df, 'RODENT_BAITING')
    df_docs = input_df.to_dict(orient='records')
    docs = []
    for df_doc in df_docs:
        docs.append({k: v for k, v in df_doc.items() if v is not None})
    db['incidents'].insert_many(docs)


def import_sanitation_complaints(input_file: str) -> None:
    """ Import the requests for sanitation code complaints to the database.

    :param input_file: The file from which to load the requests for sanitation code complaints.
    """
    print("Getting requests for sanitation code complaints")
    db = next(get_db())

    input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})

    input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                        'type_of_service_request', 'nature_of_code_violation', 'street_address',
                        'zip_code', 'x_coordinate', 'y_coordinate', 'ward', 'police_district', 'community_area',
                        'latitude', 'longitude', 'geo_location', 'historical_wards_03_15', 'zip_codes',
                        'community_areas', 'census_tracts', 'wards']
    input_df = __dataframe_normalization__(input_df, 'SANITATION_VIOLATION')
    df_docs = input_df.to_dict(orient='records')
    docs = []
    for df_doc in df_docs:
        docs.append({k: v for k, v in df_doc.items() if v is not None})
    db['incidents'].insert_many(docs)


def import_tree_debris(input_file: str) -> None:
    """ Import the requests for tree debris to the database.

    :param input_file: The file from which to load the requests for tree debris.
    """
    print("Getting requests for tree debris")
    db = next(get_db())

    input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})

    input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                        'type_of_service_request', 'tree_location', 'current_activity',
                        'most_recent_action', 'street_address', 'zip_code', 'x_coordinate', 'y_coordinate',
                        'ward', 'police_district', 'community_area', 'latitude', 'longitude',
                        'geo_location', 'historical_wards_03_15', 'zip_codes', 'community_areas',
                        'census_tracts', 'wards']
    input_df = __dataframe_normalization__(input_df, 'TREE_DEBRIS')
    df_docs = input_df.to_dict(orient='records')
    docs = []
    for df_doc in df_docs:
        docs.append({k: v for k, v in df_doc.items() if v is not None})
    db['incidents'].insert_many(docs)


def import_tree_trims(input_file: str) -> None:
    """ Import the requests for tree trims to the database.

    :param input_file: The file from which to load the requests for tree trims.
    """
    print("Getting requests for tree trims")
    db = next(get_db())

    input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})

    input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                        'type_of_service_request', 'tree_location', 'street_address', 'zip_code', 'x_coordinate',
                        'y_coordinate', 'ward', 'police_district', 'community_area', 'latitude', 'longitude',
                        'geo_location', 'historical_wards_03_15', 'zip_codes', 'community_areas',
                        'census_tracts', 'wards']
    input_df = __dataframe_normalization__(input_df, 'TREE_TRIMS')
    df_docs = input_df.to_dict(orient='records')
    docs = []
    for df_doc in df_docs:
        docs.append({k: v for k, v in df_doc.items() if v is not None})
    db['incidents'].insert_many(docs)


def import_alley_lights_out_or_street_lights_all_out(input_file: str, street_lights: bool):
    """ Import the requests for alley lights out or street lights all out (works the same for both of them) to the
    database.

    :param input_file: The file from which to load the requests for lights incidents.
    :param street_lights: Indicator if the method is called for street lights or not
    """
    db = next(get_db())

    input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})
    input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                        'type_of_service_request', 'street_address', 'zip_code', 'x_coordinate', 'y_coordinate',
                        'ward', 'police_district', 'community_area', 'latitude', 'longitude', 'geo_location',
                        'historical_wards_03_15', 'zip_codes', 'community_areas', 'census_tracts', 'wards']
    if street_lights:
        print("Getting requests for street lights all out")
        input_df = __dataframe_normalization__(input_df, 'STREET_ALL_LIGHTS')
    else:
        print("Getting requests for alley lights out")
        input_df = __dataframe_normalization__(input_df, 'ALLEY_LIGHTS')
    df_docs = input_df.to_dict(orient='records')
    docs = []
    for df_doc in df_docs:
        docs.append({k: v for k, v in df_doc.items() if v is not None})
    db['incidents'].insert_many(docs)


def import_street_lights_one_out(input_file: str):
    """ Import the requests for street lights one out to the database.

    :param input_file: The file from which to load the requests for lights incidents.
    """
    print("Getting requests for street lights one out")
    db = next(get_db())

    input_df = pd.read_csv(input_file, sep=',').replace({np.nan: None})
    input_df.columns = ['creation_date', 'status', 'completion_date', 'service_request_number',
                        'type_of_service_request', 'street_address', 'zip_code', 'x_coordinate', 'y_coordinate',
                        'ward', 'police_district', 'community_area', 'latitude', 'longitude', 'geo_location']
    input_df = __dataframe_normalization__(input_df, 'STREET_ONE_LIGHT')
    df_docs = input_df.to_dict(orient='records')
    docs = []
    for df_doc in df_docs:
        docs.append({k: v for k, v in df_doc.items() if v is not None})
    db['incidents'].insert_many(docs)


def __dataframe_normalization__(df: pd.DataFrame, request_type: str) -> pd.DataFrame:
    """ Normalizes a given dataframe to a desired condition (removes duplicate rows, convert times to timezone
    aware etc.)

    :param df: A pandas dataframe
    :param request_type: The type of the incident
    :return:  The normalized dataframe
    """
    df = df.copy(deep=True)

    df = df.drop_duplicates(['creation_date', 'status', 'completion_date', 'service_request_number',
                             'type_of_service_request', 'street_address', 'zip_code'], keep='last')

    # Normalize type_of_service_request with the given
    df['type_of_service_request'] = df['type_of_service_request'].str.replace(r'.+', request_type, regex=True)

    # Add UTC timezone to datetime fields
    df['creation_date'] = pd.to_datetime(df['creation_date'], errors='ignore')
    df['creation_date'] = df['creation_date'].dt.tz_localize("UTC")
    df['creation_date'] = df['creation_date'].astype(object).where(df['creation_date'].notnull(), None)
    df['completion_date'] = pd.to_datetime(df['completion_date'], errors='ignore')
    df['completion_date'] = df['completion_date'].dt.tz_localize("UTC")
    df['completion_date'] = df['completion_date'].astype(object).where(df['completion_date'].notnull(), None)

    for index in df.index:
        df.at[index, 'geo_location'] = {'type': 'Point',
                                        'coordinates': [df.at[index, 'longitude'], df.at[index, 'latitude']]}

    return df
