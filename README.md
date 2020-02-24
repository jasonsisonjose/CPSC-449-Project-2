# CPSC 449 Back End Engineering
## Nicholas Webster, Jason, Gilbert


### List all entries
**Definition**

`GET /entries`

**Response**

- `201 OK` on success

```json
[
  {
    "title": "this is my title",
    "text": "text goes here",
    "community": "dankmemes",
    "url": "www.nytimes.com",
    "username": "user1",
    "date": "2020-02-24T12:34:56"
  }
]
```

### Posting an entry
**Definition**

`POST /entries`

**Arguments**

- `"title":string` title that the user defines
- `"text":string` information the user defines
- `"community":string` optional specific group
- `"url":string` optional link to url
- `"username":string` username that the user defines TODO: create user db
- `"date":string` date submitted TODO: not an argument

**Response**

- `201 Created` on success

```json
{
  "title": "this is my title",
  "text": "text goes here",
  "community": "dankmemes",
  "url": "www.nytimes.com",
  "username": "user1",
  "date": "2020-02-24T12:34:56"
}
```

### Retrieve an entry
**Definition**

`GET /entries/<title>`

**Response**
-`404 Not Found` if does not exist
-`200 OK` on success

```json
{
  "title": "this is my title",
  "text": "text goes here",
  "community": "dankmemes",
  "url": "www.nytimes.com",
  "username": "user1",
  "date": "2020-02-24T12:34:56"
}
```

### Delete an entry
**Definition**

`DELETE /entries/<title>`

**Response**

-`404 Not Found` if does not exist
-`204 No Content` on success, no content to return
