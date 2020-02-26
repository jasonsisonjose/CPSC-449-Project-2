-- :name up_vote_entry :affected
UPDATE entries
SET upVotes = upVotes + 1
WHERE id = :id;
