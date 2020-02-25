-- :name entry_by_community :many
SELECT id, title, community, username, datePosted FROM entries
WHERE community = :community
ORDER BY datePosted DESC
LIMIT :numOfEntries;
