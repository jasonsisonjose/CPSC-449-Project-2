-- :name down_vote_entry :affected
UPDATE votes
SET downVotes = downVotes + 1
WHERE id = :id;