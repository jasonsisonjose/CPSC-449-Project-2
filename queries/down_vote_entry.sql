-- :name down_vote_entry :affected
UPDATE entries
SET downVotes = downVotes + 1
WHERE id = :id;