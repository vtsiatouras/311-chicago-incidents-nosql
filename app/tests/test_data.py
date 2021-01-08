from dateutil import parser


mock_docs = [{"creation_date": parser.parse("2015-04-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-04-09T00:00:00.000Z"),
              "service_request_number": "15-01207496",
              "type_of_service_request": "Abandoned Vehicle Complaint",
              "street_address": "3020 N WATERLOO CT", "zip_code": 60657,
              "ward": 44, "police_district": 19, "community_area": 6, "ssa": 8, "latitude": 41.93702589972641,
              "longitude": -87.64615132728282},
             {"creation_date": parser.parse("2015-05-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-06-09T00:00:00.000Z"),
              "service_request_number": "15-01207497",
              "type_of_service_request": "Abandoned Vehicle Complaint",
              "street_address": "3020 CAMBRIDGE ST", "zip_code": 60690,
              "ward": 45, "police_district": 20, "community_area": 6, "ssa": 8, "latitude": 43.93702589972641,
              "longitude": -86.64615132728282},
             {"creation_date": parser.parse("2015-05-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-06-09T00:00:00.000Z"),
              "service_request_number": "15-01207498",
              "type_of_service_request": "Abandoned Vehicle Complaint",
              "street_address": "3020 CAMBRIDGE ST", "zip_code": 60690,
              "ward": 45, "police_district": 20, "community_area": 6, "ssa": 8, "latitude": 44.53702589972641,
              "longitude": -84.54615132728282},
             {"creation_date": parser.parse("2015-05-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-06-09T00:00:00.000Z"),
              "service_request_number": "15-01207499",
              "type_of_service_request": "Graffiti Removal",
              "street_address": "652 W ROSCOE ST", "zip_code": 60690,
              "ward": 45, "police_district": 20, "community_area": 6, "ssa": 8, "latitude": 43.93702589972641,
              "longitude": -86.64615132728282},
             {"creation_date": parser.parse("2015-05-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-06-09T00:00:00.000Z"),
              "service_request_number": "15-01207500",
              "type_of_service_request": "Graffiti Removal",
              "street_address": "619 W CORNELIA AVE", "zip_code": 60690,
              "ward": 45, "police_district": 20, "community_area": 6, "ssa": 8, "latitude": 43.93702589972641,
              "longitude": -86.64615132728282},
             {"creation_date": parser.parse("2015-05-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-06-09T00:00:00.000Z"),
              "service_request_number": "15-01207501",
              "type_of_service_request": "Pothole in Street",
              "street_address": "437 W ROSCOE ST", "zip_code": 60690,
              "ward": 45, "police_district": 20, "community_area": 6, "ssa": 8, "latitude": 43.93702589972641,
              "longitude": -86.64615132728282},
             {"creation_date": parser.parse("2015-05-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-06-09T00:00:00.000Z"),
              "service_request_number": "15-01207502",
              "type_of_service_request": "Pothole in Street",
              "street_address": "3016 N PINE GROVE AVE", "zip_code": 60690,
              "ward": 45, "police_district": 20, "community_area": 6, "ssa": 8, "latitude": 43.93702589972641,
              "longitude": -86.64615132728282},
             {"creation_date": parser.parse("2015-05-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-06-09T00:00:00.000Z"),
              "service_request_number": "15-01207503",
              "type_of_service_request": "Pothole in Street",
              "street_address": "857 W FLETCHER ST", "zip_code": 60690,
              "ward": 45, "police_district": 20, "community_area": 6, "ssa": 8, "latitude": 43.93702589972641,
              "longitude": -86.64615132728282},
             {"creation_date": parser.parse("2015-05-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-06-09T00:00:00.000Z"),
              "service_request_number": "15-01207504",
              "type_of_service_request": "Street Light Out",
              "street_address": "2844 N CAMBRIDGE AVE", "zip_code": 60690,
              "ward": 45, "police_district": 20, "community_area": 6, "ssa": 8, "latitude": 43.93702589972641,
              "longitude": -86.64615132728282},
             {"creation_date": parser.parse("2015-05-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-06-09T00:00:00.000Z"),
              "service_request_number": "15-01207505",
              "type_of_service_request": "Street Light Out",
              "street_address": "701 W BROMPTON AVE", "zip_code": 60690,
              "ward": 45, "police_district": 20, "community_area": 6, "ssa": 8, "latitude": 43.93702589972641,
              "longitude": -86.64615132728282},
             {"creation_date": parser.parse("2015-05-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-06-09T00:00:00.000Z"),
              "service_request_number": "15-01207506",
              "type_of_service_request": "Street Light Out",
              "street_address": "2900 N BURLING ST", "zip_code": 60690,
              "ward": 45, "police_district": 20, "community_area": 6, "ssa": 8, "latitude": 43.93702589972641,
              "longitude": -86.64615132728282},
             {"creation_date": parser.parse("2015-05-08T00:00:00.000Z"),
              "status": "Completed",
              "completion_date": parser.parse("2015-06-09T00:00:00.000Z"),
              "service_request_number": "15-01207507",
              "type_of_service_request": "Alley Light Put",
              "street_address": "2847 N HALSTED ST", "zip_code": 60690,
              "ward": 45, "police_district": 20, "community_area": 6, "ssa": 8, "latitude": 43.93702589972641,
              "longitude": -86.64615132728282}
             ]