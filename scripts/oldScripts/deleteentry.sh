#!/bin/sh

if [ $1 ]
then
  curl --verbose \
       --request DELETE \
       http://localhost:5000/api/v1/entries/$1
else
  echo "Must include entry ID as argument"
  echo "EXAMPLE:"
  echo "    ./deleteentry.sh <####>"
fi
