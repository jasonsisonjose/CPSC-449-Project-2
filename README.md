# CPSC 449 Back End Engineering Project 1
## Nicholas Webster, Jason, Gilbert

### Foreman Command
`foreman start -m post-service=3,vote-service=3,caddy=1`

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



## List the n top-scoring posts to any community
**Definition**

`GET /api/v1/entries/all/top/<int:numOfEntries>`

**Response**
- `200 OK` on success
<p>&nbsp;</p>



## Given a list of post identifiers, return the list sorted by score
**Definition**

`GET /api/v1/entries/all/recent/<list:id>`

**Example**

`/api/v1/entries/scorelist/1+3+2`

**Response**
- `200 OK` on success
