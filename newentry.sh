#!/bin/sh

curl --verbose \
     --request POST \
     --header 'Content-Type: application/json' \
     --data @newentry.json \
    http://localhost:5000/api/v1/entries
