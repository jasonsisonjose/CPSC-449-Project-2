-- :name entry_by_votes :many
SELECT id, title, community, username, datePosted, upVotes, downVotes FROM entries
ORDER BY upVotes - downVotes DESC
LIMIT :numOfEntries;