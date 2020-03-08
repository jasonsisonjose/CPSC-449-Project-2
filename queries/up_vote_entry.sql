-- :name up_vote_entry :affected
UPDATE votes
SET upVotes = upVotes + 1
WHERE id = :id;
