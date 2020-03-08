-- :name report_votes :one
SELECT id, upVotes, downVotes FROM votes
where id = :id