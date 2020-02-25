-- :name entry_by_community :many
SELECT * FROM entries
WHERE community = :community;
