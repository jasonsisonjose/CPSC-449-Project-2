# Import the framework
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

# ---- CHANGE!!!---- #
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

# ---- Posting Microservice ----

# List all entries
@app.route('/api/v1/entries/all', methods=['GET'])
def all_entries():
    all_entries = queries.all_entries()
    return list(all_entries)

# GET/DELETE given an id (also shows upvotes and downvotes)
@app.route('/api/v1/entries/<int:id>', methods=['GET','DELETE'])
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

if __name__ == "__main__":
    app.run()
