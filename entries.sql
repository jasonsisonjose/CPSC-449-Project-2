-- $ sqlite3 entries.db < entries.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    id INTEGER primary key,
    title VARCHAR,
    bodyText VARCHAR,
    community VARCHAR,
    url VARCHAR,
    username VARCHAR,
    datePosted VARCHAR,
    UNIQUE(id)
);
INSERT INTO entries(id, title, bodyText, community, url, username, datePosted) VALUES(0,"title 0","bodyText 0","dankmemes","www.nytimes.com","username0","2020-02-24T12:34:56");
INSERT INTO entries(id, title, bodyText, community, url, username, datePosted) VALUES(1,"title 1","bodyText 1","dankmemes","www.latimes.com","username1","2020-02-24T12:34:57");
COMMIT;
