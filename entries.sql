-- $ sqlite3 entries.db < entries.sql

 --PRAGMA foreign_keys=ON;
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
INSERT INTO entries(id, title, bodyText, community, url, username, datePosted) VALUES(0,"title 0","bodyText 0","betaTest","www.nytimes.com","username0","2020-02-24 12:34:56");
INSERT INTO entries(id, title, bodyText, community, url, username, datePosted) VALUES(1,"first title","bodyText 1","soloSubreddit","www.latimes.com","username1","2020-02-25 12:34:57");
INSERT INTO entries(id, title, bodyText, community, url, username, datePosted) VALUES(2,"this is the second title","bodyText 2","dankmemes","www.google.com","username2","2020-02-26 12:34:57");
INSERT INTO entries(id, title, bodyText, community, url, username, datePosted) VALUES(3,"title 3","bodyText 3","dankmemes","www.facebook.com","username3","2020-02-27 12:34:57");
INSERT INTO entries(id, title, bodyText, community, url, username, datePosted) VALUES(4,"title 4","bodyText 4","dankmemes","www.news.com","username3","2020-02-28 12:34:57");
COMMIT;

BEGIN TRANSACTION;
DROP TABLE IF EXISTS votes;
CREATE TABLE votes (
    id INTEGER PRIMARY KEY,
    upVotes INTEGER,
    downVotes INTEGER,
    FOREIGN KEY (id) REFERENCES entries(id) 
);

INSERT INTO votes(id, upVotes, downVotes) VALUES(0,1,2);
INSERT INTO votes(id, upVotes, downVotes) VALUES(1,69,7);
INSERT INTO votes(id, upVotes, downVotes) VALUES(2,420,4);
INSERT INTO votes(id, upVotes, downVotes) VALUES(3,96,19);
INSERT INTO votes(id, upVotes, downVotes) VALUES(4,20,20);
COMMIT;

