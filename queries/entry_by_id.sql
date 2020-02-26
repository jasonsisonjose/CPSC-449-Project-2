-- :name entry_by_id :one
SELECT id, title, community, username, datePosted, upVotes, downVotes FROM entries
WHERE id = :id;
