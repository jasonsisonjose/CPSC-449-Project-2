-- :name delete_entry :affected
DELETE FROM entries
WHERE id = :id;
