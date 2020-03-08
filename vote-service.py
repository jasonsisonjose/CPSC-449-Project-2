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

# Upvote an entry
@app.route('/api/v1/votes/<int:id>/upvote', methods=['GET'])
def up_vote(id):
    up_vote_entry = queries.up_vote_entry(id=id)
    if up_vote_entry:
        return get_entry_with_id(id)
    else:
        return { 'message': f'Entry with id {id} can\'t be upvoted' }, status.HTTP_400_BAD_REQUEST

# Downvote an entry
@app.route('/api/v1/votes/<int:id>/downvote', methods=['GET'])
def down_vote(id):
    down_vote_entry = queries.down_vote_entry(id=id)
    if down_vote_entry:
        return get_entry_with_id(id)
    else:
        return { 'message': f'Entry with id {id} can\'t be downvoted' }, status.HTTP_400_BAD_REQUEST

# Given a list of post identifiers, return the list sorted by score
@app.route('/api/v1/votes/scorelist', methods=['POST'])
def score_list():
    entries_by_list = queries.entries_by_list(request.data)
    if entries_by_list:
        myList = list(entries_by_list)
        return myList
    else:
       return { 'message': 'Posts could not be retrieved' }, status.HTTP_400_BAD_REQUEST

# Return entry given an id
def get_entry_with_id(id):
    entry = queries.entry_by_id(id=id)
    if entry:
        return entry
    else:
        raise exceptions.NotFound()

if __name__ == "__main__":
    app.run()
