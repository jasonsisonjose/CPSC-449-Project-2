# Import the framework
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

# Import the dotenv to load variables from the environment
# to run Flask using Foreman
from dotenv import load_dotenv
load_dotenv()

# Import Redis
from flask_redis import Redis

# ---- Initialize Redis using Flask ----
app = flask_api.FlaskAPI(__name__)
app.config['REDIS_HOST'] = 'localhost'
# default port
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 0
r_server = Redis(app)
#app.config.from_envvar('APP_CONFIG')

#queries = pugsql.module('queries/')
#queries.connect(app.config['DATABASE_URL'])


#def init_db():
#    with app.app_context():
#        db = queries._engine.raw_connection()
#        with app.open_resource('entries.sql', mode='r') as f:
#            db.cursor().executescript(f.read())
#        db.commit()


# Create a Votes Set
r_server.sadd("votes",0,1,2)

# ---- Create Keys/Data for Votes Set ----
r_server.hset(0,"id",0)
r_server.hset(0,"upvotes",1)
r_server.hset(0,"downvotes",2)
r_server.hset(0, "score", int(r_server.hget(0,"upvotes")) - int(r_server.hget(0,"downvotes")))

r_server.hset(1,"id",1)
r_server.hset(1,"upvotes",420)
r_server.hset(1,"downvotes",4)
r_server.hset(1, "score", int(r_server.hget(1,"upvotes")) - int(r_server.hget(1,"downvotes")))

r_server.hset(2,"id",2)
r_server.hset(2,"upvotes",69)
r_server.hset(2,"downvotes",7)
r_server.hset(2, "score", int(r_server.hget(2,"upvotes")) - int(r_server.hget(2,"downvotes")))


# Home page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to Fake Reddit!</h1>'''


# ---- Voting Microservice ----

# GET n top-scoring entries, all communities
@app.route('/api/v1/votes/top/<int:numOfEntries>', methods=['GET'])
def get_top_scoring(numOfEntries):
    #top_entries = queries.entry_by_votes(numOfEntries=numOfEntries)

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
        #report_votes = queries.report_votes(id=id)
        # check if the hash field with the entry id exists
        report_votes = r_server.hexists(id,"upvotes")
        if report_votes:
            return r_server.hgetall(id)
        else:
            return { 'message': f'Entry with id {id} does not exist' }, status.HTTP_404_NOT_FOUND

    # using PUT method to upvote entry
    elif request.method == 'PUT':
        #up_vote_entry = queries.up_vote_entry(id=id)
        up_vote_entry = upvoteEntry(r_server,id)
        if up_vote_entry:
            return { 'message': f'Entry with id {id} has been upvoted' }, status.HTTP_200_OK
        else:
            return { 'message': f'Entry with id {id} can\'t be upvoted' }, status.HTTP_400_BAD_REQUEST

    # using PATCH method to downvote entry
    elif request.method == 'PATCH':
        #down_vote_entry = queries.down_vote_entry(id=id)
        down_vote_entry = downvoteEntry(r_server,id)
        if down_vote_entry:
             return { 'message': f'Entry with id {id} has been downvoted' }, status.HTTP_200_OK
        else:
            return { 'message': f'Entry with id {id} can\'t be downvoted' }, status.HTTP_400_BAD_REQUEST


# Given a list of post identifiers, return the list sorted by score
@app.route('/api/v1/votes/scorelist', methods=['POST'])
def score_list():
    #entries_by_list = queries.entries_by_list(request.data)
    idList = request.json['id']
    entries_by_list = queries.entries_by_list(idList=idList)
    if entries_by_list:
        return list(entries_by_list)
    else:
       return { 'message': 'Posts could not be retrieved' }, status.HTTP_400_BAD_REQUEST





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
        #keep score updated
        redisCL.hincrby(id,"score",-1)
        return hash_check
    else:
        raise exceptions.NotFound()


# Return entry given an id
def get_entry_with_id(id):
    entry = queries.entry_by_id(id=id)
    if entry:
        return entry
    else:
        raise exceptions.NotFound()
