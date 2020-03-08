#!/bin/sh

if [ $1 ]
then
  curl --verbose \
       --request PATCH \
       http://localhost:5000/api/v1/votes/$1
else
  echo "Must include entry ID as argument"
  echo "EXAMPLE:"
  echo "    ./downVoteEntry.sh <####>"
fi