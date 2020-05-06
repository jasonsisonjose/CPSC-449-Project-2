# CPSC 449 Back End Engineering Project 2
## Nicholas Webster, Jason Jose, Gilbert Paderogo

### Foreman Command
`foreman start`

### All entries have the form
```json
[
  {
    "id": "####",
    "title": "title",
    "bodyText": "bodyText",
    "community": "community",
    "url": "www.url.com",
    "username": "username",
    "date": "YYYY-MM-DD HH:MM:SS"
  }
]
```

### All votes have the form
```json
[
  {
    "id": "####",
    "upVotes": "upVotes",
    "downVotes": "downVotes"
  }
]
```

## Backend-For-Frontend
### View Recent posts from ANY community
**Definition**

`GET /all/new.rss`

**Response**
- `200 OK` on success  
<p>&nbsp;</p>

### View Recent posts from a SPECIFC community
**Definition**

`GET /<communityName>/new.rss`

**Response**
- `200 OK` on success  
<p>&nbsp;</p>

### View Top posts from ANY community
**Definition**

`GET /all/top.rss`

**Response**
- `200 OK` on success  
<p>&nbsp;</p>

### View Top posts from a SPECIFIC community 
**Definition**

`GET /<communityName>/top.rss`

**Response**
- `200 OK` on success  
<p>&nbsp;</p>

### View Hot posts from ANY community
**Definition**

`GET /all/hot.rss`

**Response**
- `200 OK` on success  

## List all entries
**Definition**

`GET /api/v1/entries/all`

**Response**
- `200 OK` on success  
<p>&nbsp;</p>



## Retrieve an entry
**Definition**

`GET /api/v1/entries/<int:id>`

**Response**
- `404 Not Found` if does not exist
- `200 OK` on success  
<p>&nbsp;</p>



## Post an entry
**Definition**

`POST /api/v1/entries`

**Response**
- `201 CREATED` on success
- `409 CONFLICT` if ID already exists  
<p>&nbsp;</p>



## Delete an entry
**Definition**

`DELETE /api/v1/entries/<int:id>`

**Response**
- `200 OK` on success  
<p>&nbsp;</p>



## List n most recent posts in a community
**Definition**

`GET /api/v1/entries/<string:community>/recent/<int:numOfEntries>`

**Response**
- `200 OK` on success  
<p>&nbsp;</p>



## List n most recent posts in all communities
**Definition**

`GET /api/v1/entries/all/recent/<int:numOfEntries>`

**Response**
- `200 OK` on success
<p>&nbsp;</p>


## Report the number of upvotes/downvotes for a post
**Definition**

`GET /api/v1/votes/<int:id>`

**Response**
- `200 OK` on success
<p>&nbsp;</p>


## Upvote a post
**Definition**

`PUT /api/v1/votes/<int:id>`

**Example**
`curl --verbose --request PUT http://localhost:5100/api/v1/votes/1`

**Response**
- `200 OK` on success
<p>&nbsp;</p>


## Downvote a post
**Definition**

`PATCH /api/v1/votes/<int:id>`

**Example**
`curl --verbose --request PATCH http://localhost:5100/api/v1/votes/1`

**Response**
- `200 OK` on success
<p>&nbsp;</p>


## List the n top-scoring posts to any community
**Definition**

`GET /api/v1/votes/top/<int:numOfEntries>`

**Response**
- `200 OK` on success
<p>&nbsp;</p>


## Given a list of post identifiers, return the list sorted by score
**Definition**

`POST /api/v1/votes/scorelist`

**Example**

`curl --verbose --request POST --header 'Content-Type: application/json' --data '{"id":[1,2,3]}' http://localhost:5100/api/v1/votes/scorelist`

**Response**
- `200 OK` on success
