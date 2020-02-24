-- :name entry_by_id :one
SELECT * FROM entries
WHERE id = :id;
