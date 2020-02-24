# CPSC 449 Back End Engineering
## Nicholas Webster, Jason, Gilbert

### List all entries
**Definition**

`GET /api/v1/entries/all`

**Response**

- `200 OK` on success

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

### Retrieve an entry
**Definition**

`GET /api/v1/entries/<int:id>`

**Response**
- `404 Not Found` if does not exist
- `200 OK` on success

```json
{
  "id": "####",
  "title": "title",
  "bodyText": "bodyText",
  "community": "community",
  "url": "www.url.com",
  "username": "username",
  "date": "YYYY-MM-DDTHH:MM:SS"
}
```
