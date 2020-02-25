# Import the framework
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

# Create instance of Flask
app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

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
    return 'Welcome to Nic\'s localhost'

# List all entries
@app.route('/api/v1/entries/all', methods=['GET'])
def all_entries():
    all_entries = queries.all_entries()
    return list(all_entries)

# GET/DELETE/PUT given an id
@app.route('/api/v1/entries/<int:id>', methods=['GET','DELETE','PUT'])
def entry(id):
    if request.method == 'GET':
        return get_entry_with_id(id)
    elif request.method == 'DELETE':
        queries.delete_entry(id=id)
        return { 'message': f'Deleted post with id {id}' }, status.HTTP_200_OK  

# General GET/POST
@app.route('/api/v1/entries', methods=['GET','POST'])
def entries():
    if request.method == 'GET':
        return filter_entries(request.args)
    elif request.method == 'POST':
        return create_entry(request.data)

# GET n most recent entries, specific community
@app.route('/api/v1/entries/<string:community>/recent/<int:numOfEntries>', methods=['GET'])
def get_community_recent(community, numOfEntries):
    community_entries = queries.entry_by_community(community=community, numOfEntries=numOfEntries)
    myList = list(community_entries)
    return myList

# GET n most recent entries, all communities
@app.route('/api/v1/entries/all/recent/<int:numOfEntries>', methods=['GET'])
def get_all_recent(numOfEntries):
    all_entries = queries.all_entries_ordered(numOfEntries=numOfEntries)
    myList = list(all_entries)
    return myList

# GET n top-scoring posts, all communities
@app.route('/api/v1/entries/all/top/<int:numOfEntries>', methods=['GET'])
def get_top_scoring(numOfEntries):
    top_entries = queries.entry_by_votes(numOfEntries=numOfEntries)
    myList = list(top_entries)
    return myList 

# Create a new entry
def create_entry(entry):
    required_fields = ['id', 'title', 'bodyText', 'community', 'url', 'username', 'datePosted']

    if not all([field in entry for field in required_fields]):
        raise exceptions.ParseError()
    try:
        entry['id'] = queries.create_entry(**entry)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return entry, status.HTTP_201_CREATED, {
        'Location': f'/api/v1/entries/{entry["id"]}'
    }

# Filter entries given user input
def filter_entries(query_parameters):
    id = query_parameters.get('id')

    query = "SELECT * FROM entries WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if not (id):
        raise exceptions.NotFound()

    query = query[:-4] + ';'

    results = queries._engine.execute(query, to_filter).fetchall()

    return list(map(dict, results))

# Return entry given an id
def get_entry_with_id(id):
    entry = queries.entry_by_id(id=id)
    if entry:
        return entry
    else:
        raise exceptions.NotFound()
