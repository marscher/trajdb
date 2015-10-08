
--
-- TABLE: CollectionOwnership
-- who owns which collection
--  

CREATE TABLE CollectionOwnership (
  collection_id int NOT NULL ,
  user_id int NOT NULL 
);

-- 
ALTER TABLE CollectionOwnership ADD CONSTRAINT pk_collection_owner UNIQUE (collection_id,user_id);
