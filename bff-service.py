# This program is responsible for creating the Backend for Frontend usage

# For testing purposes
# Assumes that Post-services are running on PORT: 8000
# Assumes that Vote-services are running on PORT: 8100

# Required views to have:
# TODO: The 25 most recent posts to a particular community
# [DONE]: The 25 most recent posts to any community
# TODO: The top 25 posts to a partiocular community, sorted by score
# TODO: The top 25 posts to any community, sorted by score
# TODO: The hot 25 posts to any community, ranked using Reddit's hot ranking algorithm


import requests
from feedgen.feed import FeedGenerator
from datetime import datetime
import flask_api


from rfeed import *
# Not using the flask-api here
from flask import Response, render_template, make_response

app = flask_api.FlaskAPI(__name__)

@app.route('/', methods=['GET'])
def home():
    return '<h1> Welcome to Reddit, here are the available viewings <h1>'


# TODO: The 25 most recent posts to a particular community
@app.route('/<string:community>/new.rss', methods=['GET'])
def community_entries():
    pass

# [DONE]: The 25 most recent posts to any community
# May have to remove the hardcoded Localhost
@app.route('/all/new.rss', methods=['GET'])
def allRecentEntries():
    postServiceResponse = requests.get('http://localhost:8000/api/v1/entries/all')
    jsonResponse = postServiceResponse.json()
    itemList = []

    # For every item in our response, we want to add it to our feed
    for item in jsonResponse:
        tempItem = Item(
            title=item['title'],
            author=item['username'],
            guid=Guid(item['id']),
            link='http://localhost:8000/api/v1/entries/' + str(item['id']),
            categories=item['community'],
            pubDate=datetime.strptime(item['datePosted'], '%Y-%m-%d %H:%M:%S')
        )
        itemList.append(tempItem)

    # Using the items we just created, we can now construct a proper feed
    feed=Feed(
    title="All Recent Community Posts",
    link="http://localhost:8000/api/v1/entries/all",
    description="For any community, here are the most recent posts",
    lastBuildDate=datetime.now(),
    items=itemList
    )

    # We create the feed into RSS format
    rssFeed = feed.rss()
    # We adjust the content-type header in the response to rss+xml
    return Response(rssFeed, mimetype='application/rss+xml')


# TODO: The top 25 posts to a partiocular community, sorted by score
@app.route('/<string:community>/top.rss', methods=['GET'])
def community_scores():
    pass

# TODO: The top 25 posts to any community, sorted by score
@app.route('/all/top.rss', methods=['GET'])
def allTopEntries():
    pass

# TODO: The hot 25 posts to any community, ranked using Reddit's hot ranking algorithm
@app.route('/all/hot.rss', methods=['GET'])
def allHottestEntries():
    pass


if __name__ == "__main__":
    app.run()
