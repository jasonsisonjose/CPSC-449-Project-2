-- :name entries_by_list :many
SELECT id, upVotes, downVotes FROM votes
WHERE id in :idList
ORDER BY upVotes - downVotes DESC;
