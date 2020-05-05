# Import the framework
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

# Import the dotenv to load variables from the environment
# to run Flask using Foreman
from dotenv import load_dotenv
load_dotenv()

# ---- Import Redis ----
#from flask_redis import Redis
import redis
# ---- Initialize Redis using Flask ----
app = flask_api.FlaskAPI(__name__)
#app.config['REDIS_HOST'] = 'localhost'
# default port
#app.config['REDIS_PORT'] = 6379
#app.config['REDIS_DB'] = 0
#r_server = Redis(app)
r_server = redis.Redis('localhost',decode_responses=True)

# ---- Create a Votes Set ----
r_server.sadd("votes",1,2,3)

# ---- Create Keys/Data for Votes Set ----
r_server.hset(1,"id",1)
r_server.hset(1,"upvotes",1)
r_server.hset(1,"downvotes",2)
r_server.hset(1, "score", int(r_server.hget(1,"upvotes")) - int(r_server.hget(1,"downvotes")))

r_server.hset(2,"id",2)
r_server.hset(2,"upvotes",420)
r_server.hset(2,"downvotes",4)
r_server.hset(2, "score", int(r_server.hget(2,"upvotes")) - int(r_server.hget(2,"downvotes")))

r_server.hset(3,"id",3)
r_server.hset(3,"upvotes",69)
r_server.hset(3,"downvotes",7)
r_server.hset(3, "score", int(r_server.hget(3,"upvotes")) - int(r_server.hget(3,"downvotes")))


# ---- Home page ----
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to Fake Reddit Voting Service!</h1>'''


# ---- Voting Microservice ----

# GET n top-scoring entries, all communities
@app.route('/api/v1/votes/top/<int:numOfEntries>', methods=['GET'])
def get_top_scoring(numOfEntries):

    # check if numOfEntries is larger than the number of keys in the Set
    if (numOfEntries > r_server.scard("votes")):
        return { 'message': 'Not enough entries to fulfill request' }, status.HTTP_400_BAD_REQUEST

    # otherwise sort the set by score and display it
    else:
        list = r_server.sort("votes",by="*->score",desc=True)
        myList = []
        for i in range(numOfEntries):
            num = int(list[i])
            myList.append(r_server.hgetall(num))

        return myList

# Report an entry's number of upvotes/downvotes, upvote or downvote the entry
@app.route('/api/v1/votes/<int:id>', methods=['GET', 'PUT', 'PATCH'])
def report_votes(id):

    if request.method == 'GET':
        # check if the hash field with the entry id exists
        report_votes = r_server.hexists(id,"upvotes")
        if report_votes:
            return r_server.hgetall(id)
        else:
            return { 'message': f'Entry with id {id} does not exist' }, status.HTTP_404_NOT_FOUND

    # using PUT method to upvote entry
    elif request.method == 'PUT':
        up_vote_entry = upvoteEntry(r_server,id)
        if up_vote_entry:
            return { 'message': f'Entry with id {id} has been upvoted' }, status.HTTP_200_OK
        else:
            return { 'message': f'Entry with id {id} can\'t be upvoted' }, status.HTTP_400_BAD_REQUEST

    # using PATCH method to downvote entry
    elif request.method == 'PATCH':
        down_vote_entry = downvoteEntry(r_server,id)
        if down_vote_entry:
             return { 'message': f'Entry with id {id} has been downvoted' }, status.HTTP_200_OK
        else:
            return { 'message': f'Entry with id {id} can\'t be downvoted' }, status.HTTP_400_BAD_REQUEST


# Given a list of post identifiers, return the list sorted by score
@app.route('/api/v1/votes/scorelist', methods=['POST'])
def score_list():
    # grab the list
    idList = request.json['id']
    scoreList = []
    for i in idList:
        # check to see if the id exists in the set
        if(r_server.hexists(i,"upvotes")):
            scoreList.append(r_server.hgetall(i))
        else:
            return { 'message': 'Posts could not be retrieved' }, status.HTTP_400_BAD_REQUEST

    #  before sorting list, we need to change the data type of score to int
    listLen = len(idList)
    for x in range(listLen):
        scoreList[x]["score"] = int(scoreList[x]["score"])


    # now we can sort the list
    newList = sorted(scoreList, key = lambda k: k['score'],reverse=True)

    return newList


# ---- Helper Functions ----

# Upvote an entry
def upvoteEntry(redisCL, id):
    hash_check = redisCL.hexists(id,"upvotes")
    if hash_check:
        redisCL.hincrby(id,"upvotes",1)
        # keep score updated
        redisCL.hincrby(id,"score",1)
        return hash_check
    else:
        raise exceptions.NotFound()


# Downvote an entry:
def downvoteEntry(redisCL, id):
    hash_check = redisCL.hexists(id,"downvotes")
    if hash_check:
        redisCL.hincrby(id,"downvotes",1)
        # keep score updated
        redisCL.hincrby(id,"score",-1)
        return hash_check
    else:
        raise exceptions.NotFound()
