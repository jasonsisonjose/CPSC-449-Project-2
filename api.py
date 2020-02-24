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

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The entry could not be found.</p>", 404

# Home page
@app.route('/', methods=['GET'])
def home():
    return 'Welcome to Nic\'s localhost'

# List all entries
@app.route('/api/v1/entries/all', methods=['GET'])
def all_entries():
    all_entries = queries.all_entries()
    return list(all_entries)

# Retrieve an entry given a unique id
@app.route('/api/v1/entries/<int:id>', methods=['GET'])
def entry(id):
    entry = queries.entry_by_id(id=id)
    if entry:
        return entry
    else:
        raise exceptions.NotFound()

# Call a GET/POST
@app.route('/api/v1/entries', methods=['GET','POST'])
def entries():
    if request.method == 'GET':
        return filter_entries(request.args)
    elif request.method == 'POST':
        return create_entry(request.data)

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
