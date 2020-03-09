#!/bin/sh

curl --verbose \
     --request POST \
     --header 'Content-Type: application/json' \
     --data @identifierList.json \
     http://localhost:5100/api/v1/votes/scorelist

curl --verbose \
     --request PUT \
     http://localhost:5100/api/v1/votes/1

curl --verbose \
     --request PATCH \
     http://localhost:5100/api/v1/votes/1
