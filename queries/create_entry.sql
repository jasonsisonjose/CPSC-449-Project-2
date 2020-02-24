-- :name create_entry :insert
INSERT INTO entries(id, title, bodyText, community, url, username, datePosted)
VALUES(:id, :title, :bodyText, :community, :url, :username, :datePosted)
