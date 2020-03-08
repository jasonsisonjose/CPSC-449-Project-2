-- :name entries_by_list :many
SELECT upVotes, downVotes FROM votes
WHERE id = :id
ORDER BY upVotes - downVotes DESC;
