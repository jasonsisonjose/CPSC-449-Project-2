-- :name entries_by_list :many
SELECT id, upVotes, downVotes FROM votes
WHERE id = :id
ORDER BY upVotes - downVotes DESC;
