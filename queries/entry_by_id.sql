-- :name entry_by_id :one
SELECT id, title, community, username, datePosted FROM entries
WHERE id = :id;
