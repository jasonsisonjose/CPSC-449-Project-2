# CPSC 449 Back End Engineering Project 1
## Nicholas Webster, Jason, Gilbert

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
    "date": "YYYY-MM-DDTHH:MM:SS"
  }
]
```

## List all entries
**Definition**

`GET /api/v1/entries/all`

**Response**
- `200 OK` on success  




## Retrieve an entry
**Definition**

`GET /api/v1/entries/<int:id>`

**Response**
- `404 Not Found` if does not exist
- `200 OK` on success  




## Post an entry
**Definition**

`POST /api/v1/entries`

**Response**
- `201 CREATED` on success
- `409 CONFLICT` if ID already exists  




## Delete an entry
**Definition**

`DELETE /api/v1/entries/<int:id>`

**Response**
- `200 OK` on success  




## List n most recent posts in a community
**Definition**

`GET /api/v1/entries/<string:community>/recent/<int:numOfEntries>`

**Response**
- `200 OK` on success  




## List n most recent posts in all communities
**Definition**

`GET /api/v1/entries/all/recent/<int:numOfEntries>`

**Response**
- `200 OK` on success  
