-- :name entries_by_list :many
SELECT id, title, community, username, datePosted, upVotes, downVotes FROM entries
WHERE id = :id
ORDER BY upVotes - downVotes DESC;
