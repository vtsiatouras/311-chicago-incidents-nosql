import datetime

from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List

from pydantic.class_validators import Any


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Incident(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    creation_date: datetime.datetime
    completion_date: Optional[datetime.datetime]
    status: str
    service_request_number: str
    type_of_service_request: str
    current_activity: Optional[str]
    most_recent_action: Optional[str]
    street_address: str
    zip_code: Optional[int]
    zip_codes: Optional[int]
    x_coordinate: Optional[float]
    y_coordinate: Optional[float]
    ward: Optional[int]
    wards: Optional[int]
    historical_wards_03_15: Optional[int]
    police_district: Optional[int]
    community_area: Optional[int]
    community_areas: Optional[int]
    ssa: Optional[int]
    census_tracts: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]

    # Abandoned Vehicles
    license_plate: Optional[str]
    vehicle_make_model: Optional[str]
    vehicle_color: Optional[str]
    days_of_report_as_parked: Optional[int]

    # Carts potholes
    number_of_elements: Optional[int]

    # Graffiti
    surface: Optional[str]

    # Trees & Graffiti
    location: Optional[str]

    # Rodent Baiting
    number_of_premises_baited: Optional[int]
    number_of_premises_w_garbage: Optional[int]
    number_of_premises_w_rats: Optional[int]

    # Sanitation Code Violation
    nature_of_code_violation: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class Citizen(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    street_address: str
    telephone_number: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class FieldWithCount(BaseModel):
    id: Any = Field(alias='_id')
    count: int


class Top3(BaseModel):
    type_of_service_request: str
    count: int


class ZipCodeTop3(BaseModel):
    zip_code: Any = Field(alias='_id')
    top_three: List[Top3]

    class Config:
        allow_population_by_field_name = True


class AverageCompletionTime(BaseModel):
    type_of_request: str = Field(alias='_id')
    average_completion_time: str
