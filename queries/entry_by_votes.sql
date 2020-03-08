-- :name entry_by_votes :many
SELECT id, upVotes, downVotes FROM votes
ORDER BY upVotes - downVotes DESC
LIMIT :numOfEntries;