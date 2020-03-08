-- :name all_entries_sorted :many
SELECT id, title, community, username, datePosted FROM entries
ORDER BY datePosted DESC
LIMIT :numOfEntries;
