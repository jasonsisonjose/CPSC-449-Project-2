# This program is responsible for creating the Backend for Frontend usage

# For testing purposes
# Assumes that Post-services are running on PORT: 5000
# Assumes that Vote-services are running on PORT: 5100
# Assumes that bff-services are running on PORT: 5200

# Required views to have:
# [DONE]: The 25 most recent posts to a particular community
# [DONE]: The 25 most recent posts to any community
# [DONE]: The top 25 posts to a partiocular community, sorted by score
# [DONE]: The top 25 posts to any community, sorted by score
# [DONE]: The hot 25 posts to any community, ranked using Reddit's hot ranking algorithm


import requests
from datetime import datetime, timedelta
import flask_api

from math import log

from rfeed import *
# Not using the flask-api here
from flask import Response

app = flask_api.FlaskAPI(__name__)

# ===================== Extending the rfeed Class ===================== #

class Votes(Extension):
    def get_namespace(self):
        return {"xlmns:votes": "http://localhost:5100/votes"}

class VotesItem(Serializable):
    def __init__ (self, totalVotes, upVotes, downVotes, hotScore=0):
        Serializable.__init__(self)

        self.totalVotes = totalVotes
        self.upVotes = upVotes
        self.downVotes = downVotes
        self.hotScore = hotScore

    def publish(self, handler):
        Serializable.publish(self,handler)

        self._write_element("totalUpvotes", self.totalVotes)
        self._write_element("upVotes", self.upVotes)
        self._write_element("downVotes", self.downVotes)

        if self.hotScore != 0:
            self._write_element("hotScore", self.hotScore)


# ===================== WEBSITE ROUTING ===================== #

@app.route('/', methods=['GET'])
def home():
    return '<h1> Welcome to Reddit, here are the available viewings <h1>'

# Weird bug where you can only do one view at a time
# [DONE]: The 25 most recent posts to a particular community
@app.route('/<string:community>/new.rss', methods=['GET'])
def community_entries(community):
    print(community)
    postRequestUrl = 'http://localhost:5000/api/v1/entries/{}/recent/25'.format(community)
    feedTitle = 'All recent posts from the r/' + community + ' community'
    feedDescription = 'For this specific community, here are the most recent posts'

    # We construct the feed from post-service only
    rssFeed = generatePostFeed(postRequestUrl, feedTitle, feedDescription)
    # We adjust the content-type header in the response to rss+xml
    return Response(rssFeed, mimetype='application/rss+xml')

# Weird bug where you can only do one view at a time
# [DONE]: The 25 most recent posts to any community
# May have to remove the hardcoded Localhost
@app.route('/all/new.rss', methods=['GET'])
def allRecentEntries():
    postRequestUrl = 'http://localhost:5000/api/v1/entries/all'
    feedTitle = 'All recent posts from all communities'
    feedDescription = 'For all community community, here are the most recent posts'

    # We construct the feed from post-service only
    rssFeed = generatePostFeed(postRequestUrl, feedTitle, feedDescription)
    # We adjust the content-type header in the response to rss+xml
    return Response(rssFeed, mimetype='application/rss+xml')


# [DONE]: The top 25 posts to a particular community, sorted by score
@app.route('/<string:community>/top.rss', methods=['GET'])
def community_scores(community):

    # Parameters: feedTitle, feedDescription, feedRequestUrl, postRequestUrl, voteRequestUrl
    feedTitle = "The top 25 posts from the " + community + " community."
    feedDescription="For the " + community + " community, here are the top scoring posts"
    feedRequestUrl='http://localhost:5200/' + community + '/top.rss'
    voteRequestUrl='http://localhost:5100/api/v1/votes/scorelist'
    postRequestUrl='http://localhost:5000/api/v1/entries/{}/recent/25'.format(community)

    # We construct the feed in rss view and return it
    rssFeed = generateTopFeed(feedTitle, feedDescription, feedRequestUrl, voteRequestUrl, postRequestUrl)
    return Response(rssFeed, mimetype='application/rss+xml')

# [DONE]: The top 25 posts to any community, sorted by score
@app.route('/all/top.rss', methods=['GET'])
def allTopEntries():

    # Parameters: feedtitle, feedRequestUrl, feedDescription, voteRequestUrl
    feedTitle = "The top 25 posts from any community."
    feedDescription = "From any community, here are the top scoring posts"
    feedRequestUrl='http://localhost:5200/all/top.rss'
    voteRequestUrl ='http://localhost:5100/api/v1/votes/top/25'
    # We need an item list to keep track of the items in the feed
    rssFeed = generateTopFeed(feedTitle,feedDescription,feedRequestUrl,voteRequestUrl)
    return Response(rssFeed, mimetype='application/rss+xml')



# TODO: The hot 25 posts to any community, ranked using Reddit's hot ranking algorithm
# Newer submission are ranked higher
# Uses Logarithmic scale, first 10 votes = next 100 = next 1000 = next 10000 etc.
@app.route('/all/hot.rss', methods=['GET'])
def allHottestEntries():
    # This is required to do some simple sorting
    hotScoreList = []

    #This is to associate the hot score with the post id
    hotScoreDict ={}
    # Get 25 most recent posts
    postRequestUrl = 'http://localhost:5000/api/v1/entries/all'
    postServiceResponse = requests.get(postRequestUrl)
    postJsonResponse = postServiceResponse.json()

    #For every post, we need the publish date, upvote, and downvote values
    for item in postJsonResponse:
        # Get the post published date
        print("Date posted: ", item['EntryDate'])
        date = datetime.strptime(item['EntryDate'], '%Y-%m-%d %H:%M:%S.%f')
        # Get the upvote and downvote number
        voteRequestUrl = 'http://localhost:5100/api/v1/votes/' + str(item['EntryID'])
        voteServiceResponse = requests.get(voteRequestUrl)
        voteJsonResponse = voteServiceResponse.json()

        print("Upvotes: ", voteJsonResponse['upvotes'])
        upVotes = int(voteJsonResponse['upvotes'])
        print("DownVotes: ", voteJsonResponse['downvotes'])
        downVotes = int(voteJsonResponse['downvotes'])
        # Get the ranking score using hot() function
        hotScore = hot(upVotes, downVotes, date)
        hotScoreList.append(hotScore)
        hotScoreDict[hotScore] = item['EntryID']

    hotScoreList.sort(reverse=True)

    # Time for feed creation
    # Params: hotScoreList (determines order), hotScoreDict
    rssFeed = generateHotFeed(hotScoreList, hotScoreDict)
    return Response(rssFeed, mimetype='application/rss+xml')



# ===================== SUPPORTING FUNCTIONS ===================== #

originDate = datetime(1970, 1, 1)

# ===================== BORROWED REDDIT CODE: https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9 ===================== #
def timeDifference(date):
    timeDiff = date - originDate
    return timeDiff.days * 86400 + timeDiff.seconds + (float(timeDiff.microseconds) / 1000000)

def voteScore(upVotes,downVotes):
    return upVotes - downVotes

def hot(upVotes,downVotes, date):
    score = voteScore(upVotes,downVotes)
    order = log(max(abs(score), 1), 10)
    sign = 1 if score > 0 else -1 if score < 0 else 0
    seconds = timeDifference(date) - 1134028003
    return round(sign * order + seconds / 45000, 7)
# ===================================================================================================================================================== #

def generateHotFeed(hotScoreList, hotScoreDict):
    itemList = []
    for rankingScore in hotScoreList:
        #Get the Post and Total Votes to create items for feed
        postRequestUrl = 'http://localhost:5000/api/v1/entries/' + str(hotScoreDict[rankingScore])
        voteRequestUrl = 'http://localhost:5100/api/v1/votes/' + str(hotScoreDict[rankingScore])

        voteServiceResponse = requests.get(voteRequestUrl)
        voteJsonResponse = voteServiceResponse.json()
        print(voteJsonResponse)
        # Using sorted ids, get the posts and create items and add them to feed

        # Find post associated with the needed id, returns 1 post
        postServiceResponse = requests.get(postRequestUrl)
        postJsonResponse = postServiceResponse.json()

        # Because we added our own custom tag: votes, we create the item here
        # We pass in three params: totalVotes, upVotes, downVotes
        votes_item = VotesItem(
        voteJsonResponse['score'],
        voteJsonResponse['upvotes'],
        voteJsonResponse['downvotes'],
        rankingScore
        )

        # Create an item based on the post
        tempItem= Item(
            title=postJsonResponse['EntryTitle'],
            author=postJsonResponse['Username'],
            guid=Guid(postJsonResponse['EntryID']),
            link='http://localhost:5100/api/v1/entries/' + str(postJsonResponse['EntryID']),
            categories=postJsonResponse['Community'],
            pubDate=datetime.strptime(postJsonResponse['EntryDate'], '%Y-%m-%d %H:%M:%S.%f'),
            extensions=[votes_item]
        )
        # Add the item to the feed
        itemList.append(tempItem)
        # Using the items we just created, we can now construct a proper feed
    feed=Feed(
    title="Hottest Posts from any community",
    link='http://localhost:5200/all/hot.rss',
    description='These are the hottest posts right now, get them while they are fresh!',
    lastBuildDate=datetime.now(),
    items=itemList,
    extensions= [Votes()]
    )
    rssFeed = feed.rss()
    return rssFeed




def generateTopFeed(feedTitle, feedDescription, feedRequestUrl, voteRequestUrl='', postRequestUrl=''):
    # If the postrequesturl isn't empty, then go ahead and do the top 25 posts in a SPECIFIC community
    if postRequestUrl != '' and voteRequestUrl != '':
        # Initialize a list for post ids and a list for items in feed
        postIdList = []
        itemList = []

        # Get id's of the most recent 25 posts to a community
        postServiceResponse = requests.get(postRequestUrl)
        postJsonResponse = postServiceResponse.json()

        for item in postJsonResponse:
            postIdList.append(item['EntryID'])

        # Send ids to voting
        voteServiceResponse = requests.post(voteRequestUrl, json={'id': postIdList})
        voteJsonResponse = voteServiceResponse.json()

        # Using sorted ids, get the posts and create items and add them to feed
        for item in voteJsonResponse:
            # Find post associated with the needed id, returns 1 post
            postRequestUrl = 'http://localhost:5000/api/v1/entries/' + str(item['id'])
            postServiceResponse = requests.get(postRequestUrl)
            postJsonResponse = postServiceResponse.json()

            # Because we added our own custom tag: votes, we create the item here
            # We pass in three params: totalVotes, upVotes, downVotes
            votes_item = VotesItem(item['score'], item['upvotes'], item['downvotes'])

            # Create an item based on the post
            tempItem= Item(
                title=postJsonResponse['EntryTitle'],
                author=postJsonResponse['Username'],
                guid=Guid(postJsonResponse['EntryID']),
                link='http://localhost:5100/api/v1/votes/' + str(postJsonResponse['EntryID']),
                categories=postJsonResponse['Community'],
                pubDate=datetime.strptime(postJsonResponse['EntryDate'], '%Y-%m-%d %H:%M:%S.%f'),
                extensions=[votes_item]
            )
            # Add the item to the feed
            itemList.append(tempItem)
        # Using the items we just created, we can now construct a proper feed
        feed=Feed(
        title=feedTitle,
        link=feedRequestUrl,
        description=feedDescription,
        lastBuildDate=datetime.now(),
        items=itemList,
        extensions= [Votes()]
        )
        rssFeed = feed.rss()
        return rssFeed
    # Do the top 25 view for any community
    elif postRequestUrl == '' and voteRequestUrl != '':
        itemList = []
        # First we need to get the id of the posts that have the top scores
        voteServiceResponse = requests.get(voteRequestUrl)
        # We have to make sure that the response is in json format so we can work with it
        voteJsonResponse = voteServiceResponse.json()

        for item in voteJsonResponse:
            # Find post associated with the needed id, returns 1 post
            postRequestUrl = 'http://localhost:5000/api/v1/entries/' + str(item['id'])
            postServiceResponse = requests.get(postRequestUrl)
            postJsonResponse = postServiceResponse.json()
            # Because we added our own custom tag: votes, we create the item here
            # We pass in three params: totalVotes, upVotes, downVotes
            votes_item = VotesItem(
                item['score'],
                item['upvotes'],
                item['downvotes']
            )

            # Create an item based on the post
            tempItem= Item(
                title=postJsonResponse['EntryTitle'],
                author=postJsonResponse['Username'],
                guid=Guid(postJsonResponse['EntryID']),
                link='http://localhost:5100/api/v1/votes/' + str(postJsonResponse['EntryID']),
                categories=postJsonResponse['Community'],
                pubDate=datetime.strptime(postJsonResponse['EntryDate'], '%Y-%m-%d %H:%M:%S.%f'),
                extensions=[votes_item]
            )
            # Add the item to the feed
            itemList.append(tempItem)
        # Using the items we just created, we can now construct a proper feed
        feed=Feed(
        title=feedTitle,
        link=feedRequestUrl,
        description=feedDescription,
        lastBuildDate=datetime.now(),
        items=itemList
        )

        # We create the feed into RSS format
        rssFeed = feed.rss()
        return rssFeed

def generatePostFeed(feedRequestUrl, feedTitle, feedDescription):
    postServiceResponse = requests.get(feedRequestUrl)
    jsonResponse = postServiceResponse.json()
    itemList = []

    # For every item in our response, we want to add it to our feed
    for item in jsonResponse:
        tempItem = Item(
            title=item['EntryTitle'],
            author=item['Username'],
            guid=Guid(item['EntryID']),
            link='http://localhost:5000/api/v1/entries/' + str(item['EntryID']),
            categories=item['Community'],
            pubDate=datetime.strptime(item['EntryDate'], '%Y-%m-%d %H:%M:%S.%f')
        )
        itemList.append(tempItem)

    # Using the items we just created, we can now construct a proper feed
    feed=Feed(
    title=feedTitle,
    link=feedRequestUrl,
    description=feedDescription,
    lastBuildDate=datetime.now(),
    items=itemList
    )

    # We create the feed into RSS format
    rssFeed = feed.rss()

    return rssFeed


if __name__ == "__main__":
    app.run()
