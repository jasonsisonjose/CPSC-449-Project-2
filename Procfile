post-service: gunicorn3 -b localhost:$PORT --access-logfile - post-service:app
vote-service: gunicorn3 -b localhost:$PORT --access-logfile - vote-service:app
bff-service: gunicorn3 -b localhost:$PORT --access-logfile - bff-service:app
db: java -Djava.library.path=./dynamodb_local_latest/DynamoDBLocal_lib -jar dynamodb_local_latest/DynamoDBLocal.jar -sharedDb