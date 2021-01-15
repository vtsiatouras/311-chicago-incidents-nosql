# 311 Chicago Incidents noSQL

[![Django CI](https://github.com/VangelisTsiatouras/311-chicago-incidents-nosql/workflows/FastAPI%20CI/badge.svg)](https://github.com/VangelisTsiatouras/311-chicago-incidents-nosql/actions)  [![codecov](https://codecov.io/gh/VangelisTsiatouras/311-chicago-incidents-nosql/branch/main/graph/badge.svg?token=0RCQE0L9RO)](https://codecov.io/gh/VangelisTsiatouras/311-chicago-incidents-nosql)  [![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)  [![mongodb](https://img.shields.io/badge/mongodb-4.4.x-589636.svg)](https://img.shields.io/badge/mongodb-4.4.x-589636.svg)

This repository contains a FastAPI application that connects to a noSQL Mongo Database and process some metrics for the incidents that happen to Chicago City.

All the data used for the development can be found [here](https://www.kaggle.com/chicago/chicago-311-service-requests
). Also I have uploaded some of these data inside this repository, which can be found [here](https://github.com/VangelisTsiatouras/311-chicago-incidents-nosql/tree/main/assist_material/datasets/zip).

## Demo


## FastAPI Application

### Installation from source

This section contains the installation instructions in order to set up a local development environment. The instructions
have been validated for Ubuntu 20.04.

First, install all required software:

MongoDB _detailed instructions [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)_

```bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
```

Python 3.7+

```bash
sudo apt update
sudo apt install git python3 python3-pip python3-dev
```

The project dependencies are managed with [pipenv](https://docs.pipenv.org/en/latest/). You can install it with:

```bash
pip install --user pipenv
```

`pipenv` should now be in your `PATH`. If not, logout and log in again. Then install all dependencies with:

```bash
pipenv install --dev
```

Then you can enable the python environment with:

```bash
pipenv shell
```

All commands from this point forward require the python environment to be enabled.

### Environment variables

The project uses environment variables in order to keep private data like user names and passwords out of source
control. You can either set them at system level, or by creating a file named `.env` at the root of the repository. 
The required environment variables for development are:

* `MONGO_USER`: The database user
* `MONGO_PASSWORD`: The database user password 
* `MONGO_DB`: The database host. _For local development use_ `localhost`
* `MONGO_HOST`: The database name.
* `MONGO_PORT`: The database port.

### Local Development
In order to run the project on your workstation, you must create a database named according to the value of the
`MONGO_DB` environment variable, at the host that is specified by the `MONGO_HOST` environment variable. Initially you must a create the database and a user:

```
mongo
use chicago_incidents
db.createUser({user: "<USER_NAME>", pwd: "<USER_PASSWORD>", roles: [{role: "readWrite", db: "chicago_incidents"}]})
```

After you create the database, you can populate it with the initial data with:

```bash
python data_import.py [csv_files]
```

where `csv_files` is the path of the csv files (one or more) to import to the database

_Example_
```bash
python data_import.py ./assist_material/datasets/csv/311-service-requests-abandoned-vehicles.csv ./assist_material/datasets/csv/311-service-requests-street-lights-all-out.csv ./assist_material/datasets/csv/311-service-requests-street-lights-one-out.csv ./assist_material/datasets/csv/311-service-requests-alley-lights-out.csv ./assist_material/datasets/csv/311-service-requests-garbage-carts.csv ./assist_material/datasets/csv/311-service-requests-pot-holes-reported.csv ./assist_material/datasets/csv/311-service-requests-graffiti-removal.csv ./assist_material/datasets/csv/311-service-requests-rodent-baiting.csv ./assist_material/datasets/csv/311-service-requests-sanitation-code-complaints.csv ./assist_material/datasets/csv/311-service-requests-tree-debris.csv ./assist_material/datasets/csv/311-service-requests-tree-trims.csv
```

The importing takes approximately 2000 seconds (tested on i7-2600, 16gb RAM).

Now you can run the web server with:

```bash
uvicorn app.main:app
```

The API is available at http://127.0.0.1:8000/api/v1/

The documentation Swagger page of the API is available at http://127.0.0.1:8000/docs or with ReDoc http://127.0.0.1:8000/redoc

Also the Django Admin page is available at http://127.0.0.1:8000/admin/


## Installation using Docker

I recommend this way of installation in order to keep your machine clean from packages that you may not use ever again. 
 
Initially, install [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) (click the link to see
 instructions) & [Docker Compose](https://docs.docker.com/compose/install/) in order to build the project.
 
__Set up the `.env` at the root of the repository!__
* `MONGO_USER`: The database user
* `MONGO_PASSWORD`: The database user password 
* `MONGO_HOST`: `mongodb` _The host name __must__ be `mongodb`_
* `MONGO_PORT`: 27018 _You must use this port_
* `MONGO_DB`: The database name.

Then just execute the following:

```bash
docker-compose up --build
```

Then you have the database & the API up and running!

In order to perform the import of the data you can log in to the running docker container and perform the process
 manually.

```bash
docker exec -it api bash
```

Now you have access to all the files of the API. __You can now run the import command as mentioned above in the Local
Development section.__

The database is exposed at mongodb://localhost:27018/

The API & the documentation pages page are available to the same addresses that referred above.

## Database Report

### Schema

The below json are just a representation of the documents that are stored to the database. 

Incidents Collection

```text
{
  "_id":{"$oid":"id"},
  "creation_date":{"$date":"YYYY-MM-DDTHH:MM:SS.000Z"},
  "status":"string",
  "completion_date":{"$date":"YYYY-MM-DDTHH:MM:SS.000Z"},
  "service_request_number":"string",
  "type_of_service_request":"string", // Normalized with ABANDONDED_VEHICLE, GARBAGE_CARTS, LIGHTS_ALL_OUT etc.
  "street_address":"3020 N WATERLOO CT",
  "zip_code":"int",
  "zip_codes":"int",
  "ward":"int",
  "wards":"int",
  "historical_wards_03_15":"int",
  "police_district":"int",
  "community_area":"int",
  "community_areas":"int",
  "ssa":"int",
  "census_tracts":"int",
  "geo_location":{"type":"Point","coordinates":["longitude/double","latitude/double"]},
  "x_coordinate":"double",
  "y_coordinate":"double",
  
  // List of ObjectIDs of citizens that voted this incident
  "voted_by":[{"$oid":"id"},{"$oid":"id"}],
  "total_votes":"int",
  
  // Optional  
  "current_activity":"string",
  "most_recent_action":"string",

  // ABANDONED_VEHICLE
  "license_plate":"string",
  "vehicle_make_model":"string",
  "vehicle_color":"string",
  "days_of_report_as_parked":"int",
  
  // POTHOLE or GARBAGE_CART
  "number_of_elements": "int",
  
  // GRAFFITI
  "surface":"str",

  //TREE & GRAFFITI
  "location":"str",

  //RODENT_BAITING
  "number_of_premises_baited":"int",
  "number_of_premises_w_garbage":"int",
  "number_of_premises_w_rats":"int",

  // SANITATION_VIOLATION
  "nature_of_code_violation":"str"
}
```

Citizens Collection

```text
{
  "_id":{"$oid":"id"},
  "name":"string",
  "street_address":"string",
  "telephone_number":"string",
  
  // List of ObjectIDs of incidents that this user voted
  "voted_incidents":[{"$oid":"id"},{"$oid":"id"}],
  
  // The total number of votes of this user
  "total_votes":"int",
  
  // List-Set that contains all the wards of the incidents that this user voted
  "wards":["int"],
  
  // The total number of wards
  "total_wards":"int"
}
```

__Indexes__

Incidents Collection

```python
db['incidents'].create_index([('type_of_service_request', pymongo.ASCENDING)])
db['incidents'].create_index([('creation_date', pymongo.ASCENDING)])
db['incidents'].create_index([('type_of_service_request', pymongo.ASCENDING), ('creation_date', pymongo.ASCENDING)])
db['incidents'].create_index([('geo_location', pymongo.GEOSPHERE)])
db['incidents'].create_index([('total_votes', pymongo.ASCENDING)])
```

Citizens Collection

```python
db['citizens'].create_index([('total_votes', pymongo.ASCENDING)])
db['citizens'].create_index([('total_wards', pymongo.ASCENDING)])
db['citizens'].create_index([('telephone_number', pymongo.ASCENDING)])
db['citizens'].create_index([('name', pymongo.ASCENDING)])
```


Some info about the schema and the decisions that were made in order to conclude to this state.


### Queries

1. Find the total requests per type that were created within a specified time range and sort them in a descending order.

    ```python
    cursor = db['incidents'].aggregate([
        {
            '$match': {
                'creation_date': {'$gte': start_date, '$lte': end_date}
            }
        },
        {
            '$project': {
                '_id': 1,
                'type_of_service_request': 1
            }
        },
        {
            '$group': {
                '_id': '$type_of_service_request',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {
                'count': -1
            }
        }
    ])
    ```
    
2. Find the total requests per day for a specific request type and time range.

    ```python
    cursor = db['incidents'].aggregate([
        {
            '$match': {
                '$and': [
                    {'type_of_service_request': request_type},
                    {'creation_date': {'$gte': start_date, '$lte': end_date}}
                ]
            }
        },
        {
            '$project': {
                '_id': 1, 'creation_date': 1
            }
        },
        {
            '$group': {
                '_id': '$creation_date',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {
                '_id': -1
            }
        }
    ])
    ```

3. Find the three most common service requests per zipcode for a specific day.

    ```python
    cursor = db['incidents'].aggregate([
        {
            '$match': {'creation_date': date}
        },
        {
            '$project': {
                'type_of_service_request': 1,
                'zip_code': 1
            }
        },
        {  # Create counts per type and zipcode
            '$group': {
                '_id': {
                    'type_of_service_request': '$type_of_service_request',
                    'zip_code': '$zip_code'
                },
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {
                '_id.zip_code': 1, 'count': -1
            }
        },
        {  # Group types & counts per zipcode inside an array
            '$group': {
                '_id': '$_id.zip_code',
                'counts': {
                    '$push': {
                        'type_of_service_request': '$_id.type_of_service_request',
                        'count': '$count'
                    }
                }
            }
        },
        {  # Select first 3 elements of each array
            '$project': {
                'top_three': {'$slice': ['$counts', 3]}}
        }
    ])
    ```

4. Find the three least common wards with regards to a given service request type.

    ```python
    cursor = db['incidents'].aggregate([
        {
            '$match': {
                '$and': [
                    {'type_of_service_request': request_type},
                    {'ward': {'$exists': 'true'}}  # Exclude records with no ward
                ]
            }
        },
        {
            '$project': {
                'ward': 1
            }
        },
        {
            '$group': {
                '_id': '$ward',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {
                'count': 1
            }
        },
        {
            '$limit': 3
        }
    ])
    ```

5. Find the average completion time per service request for a specific date range.

    ```python
    cursor = db['incidents'].aggregate([
        {
            '$match': {
                '$and': [
                    {'creation_date': {'$gte': start_date, '$lte': end_date}},
                    {'creation_date': {'$exists': 'true'}},
                    {'completion_date': {'$exists': 'true'}}
                ]
            }
        },
        {
            '$project': {
                'creation_date': 1,
                'completion_date': 1,
                'type_of_service_request': 1
            }
        },
        {
            '$group': {
                '_id': '$type_of_service_request',
                'average_completion_time': {
                    '$avg': {
                        '$subtract': [
                            '$completion_date', '$creation_date'
                        ]
                    }
                }
            }
        },
        {
            '$sort': {
                '_id': 1
            }
        }
    ])
    ```

6. Find the most common service request in a specified bounding box for a specific day. You are encouraged to use GeoJSON objects and Geospatial Query Operators.

    ```python
    cursor = db['incidents'].aggregate([
        {
            '$match': {
                '$and': [
                    {'creation_date': date},
                    {
                        'geo_location.coordinates': {
                            '$geoWithin': {
                                '$box': [
                                    [point_a_longitude, point_a_latitude],
                                    [point_b_longitude, point_b_latitude]
                                ]
                            }
                        }
                    }
                ]
            }
        },
        {
            '$project': {
                'type_of_service_request': 1
            }
        },
        {
            '$group': {
                '_id': '$type_of_service_request',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {
                'count': -1
            }
        },
        {
            '$limit': 1
        }
    ])
    ```

7. Find the fifty most upvoted service requests for a specific day.

    ```python
    cursor = db['incidents'].aggregate([
        {
            '$match': {
                'creation_date': date
            }
        },
        {
            '$project': {
                '_id': 1,
                'total_votes': 1
            }
        },
        {
            '$sort': {
                'total_votes': -1
            }
        },
        {
            '$limit': 50
        }
    ])
    ```

8. Find the fifty most active citizens, with regard to the total number of upvotes.
    
    ```python
    cursor = db['citizens'].aggregate([
        {
            '$project': {
                '_id': 1,
                'total_votes': 1
            }
        },
        {
            '$sort': {
                'total_votes': -1
            }
        },
        {
            '$limit': 50
        }
    ])
    ```

9. Find the top fifty citizens, with regard to the total number of wards for which they have upvoted an incidents.

    ```python
    cursor = db['citizens'].aggregate([
        {
            '$project': {
                '_id': 1,
                'total_wards': 1
            }
        },
        {
            '$sort': {
                'total_wards': -1
            }
        },
        {
            '$limit': 50
        }
    ])
    ```
   
10. Find all incident ids for which the same telephone number has been used for more than one names.
   
    ```python
    cursor = db['citizens'].aggregate([
        {
            '$group': {
                '_id': '$telephone_number',
                'citizen_ids': {'$push': '$_id'},
                'count': {'$sum': 1}
            }
        },
        {   # If a phone number appears more than once
            '$match': {
                '_id': {'$ne': 'null'},
                'count': {'$gt': 1}
            }
        },
        {   # "Self Join' to citizens collection with the IDs we retrieved above
            '$lookup': {
                'from': 'citizens',
                'localField': 'citizen_ids',
                'foreignField': '_id',
                'as': 'same_phone_citizens'
            }
        },
        {   # Expand joined array to documents
            '$unwind': '$same_phone_citizens'
        },
        {   # Group by _id (phone number) and append incident IDs to array
            '$group': {
                '_id': '$_id',
                'incidents': {'$push': '$same_phone_citizens.voted_incidents'},
            }
        },
        {   # Deduplicate incident IDs using reduce
            '$project': {
                'incident_ids': {
                    '$reduce': {
                        'input': '$incidents',
                        "initialValue": [],
                        "in": {"$setUnion": ["$$this", "$$value"]}
                    }
                }
            }
        }
    ])
    ```
   
11. Find all the wards in which a given name has casted a vote for an incident taking place in it.

    ```python
    cursor = db['citizens'].aggregate([
        {
            '$match': {
                'name': name
            }
        },
        {
            '$project': {
                '_id': '$name',
                'wards': 1
            }
        }
    ])
    ```
