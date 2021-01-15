#!/bin/sh

echo 'Creating application user and db'

mongo --host localhost \
  --port 27017 \
  -u "${MONGO_USER}" \
  -p "${MONGO_PASSWORD}" \
  --authenticationDatabase admin \
  --eval "db=db.getSiblingDB('${MONGO_DB}');db.createUser({user:'${MONGO_USER}', pwd:'${MONGO_PASSWORD}', roles:[{role:'readWrite', db: '${MONGO_DB}'}]});"
