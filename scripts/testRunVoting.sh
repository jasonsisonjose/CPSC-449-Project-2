#!/bin/sh

curl --verbose \
     --request POST \
     --header 'Content-Type: application/json' \
     --data @identifierList.json \
     http://localhost:5000/api/v1/votes/scorelist

curl --verbose \
     --request GET \
     http://localhost:5000/api/v1/votes/1

curl --verbose \
     --request PUT \
     http://localhost:5000/api/v1/votes/1

curl --verbose \
     --request PATCH \
     http://localhost:5000/api/v1/votes/1
