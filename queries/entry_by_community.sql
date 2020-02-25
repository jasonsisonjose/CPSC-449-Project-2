-- :name entry_by_community :many
SELECT * FROM entries
WHERE community = :community
ORDER BY datePosted DESC
LIMIT :numOfEntries;
