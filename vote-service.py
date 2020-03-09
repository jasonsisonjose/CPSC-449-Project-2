# Import the framework
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

# ---- CHANGE!!! ---- #
# Import the dotenv to load variables from the environment
# to run Flask using Foreman
from dotenv import load_dotenv
load_dotenv()

# Custom Converter
from werkzeug.routing import BaseConverter

# Custom Class to use "list" variable in URL converter
class ListConverter(BaseConverter):

    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):
        return '+'.join(super(ListConverter,self).to_url(value)
                            for value in values)


# Create instance of Flask using the Flask API
app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

# Custom converter for grabbing a list of post identifiers
app.url_map.converters['list'] = ListConverter

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('entries.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Home page
@app.route('/', methods=['GET'])
def home():
    #return 'Welcome to Nic\'s localhost'
    return '''<h1>Welcome to Fake Reddit!</h1>
            <h2>Yeet</h2>'''


# ---- Voting Microservice ----

# GET n top-scoring entries, all communities
@app.route('/api/v1/votes/top/<int:numOfEntries>', methods=['GET'])
def get_top_scoring(numOfEntries):
    top_entries = queries.entry_by_votes(numOfEntries=numOfEntries)
    myList = list(top_entries)
    return myList

# Report an entry's number of upvotes/downvotes, upvote or downvote the entry
@app.route('/api/v1/votes/<int:id>', methods=['GET', 'PUT', 'PATCH'])
def report_votes(id):
    if request.method == 'GET':
        report_votes = queries.report_votes(id=id)
        return report_votes
    # using PUT method to upvote entry
    elif request.method == 'PUT':
        up_vote_entry = queries.up_vote_entry(id=id)
        if up_vote_entry:
            return { 'message': f'Entry with id {id} has been upvoted' }, status.HTTP_200_OK
        else:
            return { 'message': f'Entry with id {id} can\'t be upvoted' }, status.HTTP_400_BAD_REQUEST
    # using PATCH method to downvote entry
    elif request.method == 'PATCH':
        down_vote_entry = queries.down_vote_entry(id=id)
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

# Return entry given an id
def get_entry_with_id(id):
    entry = queries.entry_by_id(id=id)
    if entry:
        return entry
    else:
        raise exceptions.NotFound()
