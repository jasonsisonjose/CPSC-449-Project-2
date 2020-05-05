# Import the framework
import flask_api
from flask import request
from flask_api import status, exceptions
from flask_dynamo import Dynamo
from flask import Flask
import boto3
import datetime

# Import the dotenv to load variables from the environment
# to run Flask using Foreman
from dotenv import load_dotenv
load_dotenv()

app = flask_api.FlaskAPI(__name__)

################################### ROUTING ####################################
# Home page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to Fake Reddit!</h1>'''

# List all entries
@app.route('/api/v1/entries/all', methods=['GET'])
def all_entries():
    allEntries = Get_All_Entries('entries', dynamoDbResource)
    return list(allEntries)

# GET/DELETE given an id (also shows upvotes and downvotes)
@app.route('/api/v1/entries/<int:id>', methods=['GET','DELETE'])
def entry(id):
    if request.method == 'GET':
        return Get_Entry('entries', dynamoDbResource, id)
    elif request.method == 'DELETE':
        Delete_Entry('entries', dynamoDbResource, id)
        return { 'message': f'Deleted post with id {id}' }, status.HTTP_200_OK

# General GET/POST
@app.route('/api/v1/entries', methods=['GET','POST'])
def entries():
    if request.method == 'GET':
        num = int(request.args.get('n', 2))
        numRecentEntries = Get_n_Recent_Entries('entries', dynamoDbResource, num)
        return list(numRecentEntries)
    elif request.method == 'POST':
        username    = str(request.data.get('username',''))
        entryTitle  = str(request.data.get('entryTitle',''))
        content     = str(request.data.get('content',''))
        community   = str(request.data.get('community',''))
        url         = str(request.data.get('url',''))
        input_json = Create_Entry('entries', dynamoDbResource, username, entryTitle, content, community, url)

# GET n most recent entries, specific community
@app.route('/api/v1/entries/<string:community>/recent/<int:numOfEntries>', methods=['GET'])
def get_community_recent(community, numOfEntries):
    nRecentEntriesInCommunity = Get_n_Recent_Entries_by_Community('entries',dynamoDbResource, numOfEntries, community)
    return list(nRecentEntriesInCommunity)

# GET n most recent entries, all communities
@app.route('/api/v1/entries/all/recent/<int:numOfEntries>', methods=['GET'])
def get_all_recent(numOfEntries):
    nRecentEntriesAll = Get_n_Recent_Entries('entries',dynamoDbResource, numOfEntries)
    return list(nRecentEntriesAll)
################################################################################

############################# POSTING Microservice #############################
def Create_Table(tableName, dynamoDbClient, dynamoDbResource):
    myTable = dynamoDbClient.create_table(
        TableName = tableName,
        AttributeDefinitions=[
            {
                'AttributeName': 'EntryID',
                'AttributeType': 'N'
            }                        
        ],
        KeySchema=[
            {
                'AttributeName': 'EntryID',
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits': 100,
            'WriteCapacityUnits': 100,
        }
    )
    dynamoDbResource.meta.client.get_waiter('table_exists').wait(TableName=tableName)

def Delete_Table(tableName, dynamoDbResource):
    myTable = dynamoDbResource.Table(tableName)
    myTable.delete()

def List_All_Tables(dynamoDbClient):
    return dynamoDbClient.list_tables()['TableNames'] 

def Search_Table (tableName, dynamoDbResource):
    allEntries = []
    myTable = dynamoDbResource.Table(tableName)

    resp = myTable.scan(TableName=tableName)
    items = resp['Items']
    items.sort()
    i = 0
    while i < len(items):
        allEntries.append(items[i])
        i += 1
    return allEntries

def Table_Size(tableName, dynamoDbResource):
    myTable = dynamoDbResource.Table(tableName)
    return myTable.item_count

def Create_Entry(tableName, dynamoDbResource, username, entryTitle, content, community, url):
    tableLength = Table_Size(tableName, dynamoDbResource)
    if tableLength == 0:
        last_EntryID = 0
    else:
        allEntries = Get_All_Entries(tableName, dynamoDbResource)
        last_EntryID = 1
        for entry in allEntries:
            if entry['EntryID']> last_EntryID:
                last_EntryID = entry['EntryID']
         
    currentID = last_EntryID + 1
    currentDateTime = datetime.datetime.now()
    currentDateTimeStr = str(currentDateTime)
    input_json = {
        'EntryID'     : currentID, 
        'Username'    : username,
        'EntryTitle'  : entryTitle,
        'EntryDate'   : currentDateTimeStr,
        'Content'     : content,
        'Community'   : community,
        'url'         : url
    }
    myTable = dynamoDbResource.Table(tableName)
    myTable.put_item(Item = input_json)
    return input_json

def Get_Entry(tableName, dynamoDbResource, entryID):
    try:
        myTable = dynamoDbResource.Table(tableName)
        getEntry = myTable.get_item(
            Key = {'EntryID':entryID}
        )
        return getEntry['Item']
    except:
        print('Entry does not exist')

def Get_All_Entries(tableName, dynamoDbResource):
    allEntries = []
    myTable = dynamoDbResource.Table(tableName)

    resp = myTable.scan(TableName=tableName)
    items = resp['Items']
    i = 0
    while i < len(items):
        allEntries.append (items[i])
        i += 1

    allEntriesSorted = sorted(allEntries, key=lambda k: k['EntryID'])
    return allEntriesSorted

def Get_n_Recent_Entries(tableName, dynamoDbResource, n):
    allEntries = Get_All_Entries(tableName, dynamoDbResource)

    tableLength = Table_Size(tableName, dynamoDbResource)
    run = tableLength - 1
    nRecentEntries = []

    i = 0
    while i < n:
        try:
            nRecentEntries.append(allEntries[run])
            i += 1
            if run > 0:
                run -= 1
            else:
                break
        except:
            run -= 1
            pass
    return nRecentEntries

def Get_n_Recent_Entries_by_Community(tableName, dynamoDbResource, n, community):
    
    allEntries = Get_All_Entries(tableName, dynamoDbResource)
    tableLength = Table_Size(tableName, dynamoDbResource)
    run = tableLength - 1
    nRecentEntriesByCommunity = []

    i = 0
    while i < n:
        try:
            if allEntries[run]['Community'] == community:
                nRecentEntriesByCommunity.append(allEntries[run])
                i += 1

            if run > 0:
                run -= 1
            else:
                break
        except:
            i += 1
            pass
    return nRecentEntriesByCommunity

def Delete_Entry(tableName, dynamoDbResource, entryID):
    myTable = dynamoDbResource.Table(tableName)
    myTable.delete_item(Key= {'EntryID':entryID})

def Delete_All_Entries(tableName, dynamoDbResource):
    entryID = 1
    while entryID < 100:
        Delete_Entry(tableName, dynamoDbResource, entryID)
        entryID += 1

def Create_First_Three_Entries(tableName, dynamoDbResource):
    input_json = Create_Entry(tableName, dynamoDbResource, 'username2', '001 post title', 'this is the zeroth content 001', 'dankMemes', 'www.runescape001.com')
    input_json = Create_Entry(tableName, dynamoDbResource, 'user2', 'title 002 post', 'first contnet 002', 'dankMemes', 'www.csuf002.com')
    input_json = Create_Entry(tableName, dynamoDbResource, 'name3', 'post title 003', 'second 003 contest', 'notDank', 'www.cpsc449003.com')
################################################################################

############################## Initialize Dynamo ###############################
# Create instance of Flask using the Flask API
# app = flask_api.FlaskAPI(__name__)

tableName = 'entries'
dynamoDbClient = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
dynamoDbResource = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

app.config['DYNAMO_TABLES'] = [
    dict(
        TableName=tableName,
        KeySchema=[dict(AttributeName='EntryID', KeyType='HASH')],
        AttributeDefinitions=[dict(AttributeName='EntryID', AttributeType='N')],
        ProvisionedThroughput=dict(ReadCapacityUnits=100, WriteCapacityUnits=100)
    ) 
]

@app.cli.command('init')
def init_db():
    existingTables = List_All_Tables(dynamoDbClient)

    if tableName in existingTables:
        Delete_All_Entries(tableName, dynamoDbResource)
        Delete_Table(tableName, dynamoDbResource)

    Create_Table(tableName, dynamoDbClient, dynamoDbResource)
    Create_First_Three_Entries(tableName, dynamoDbResource)
################################################################################

if __name__ == "__main__":
    app.run()
