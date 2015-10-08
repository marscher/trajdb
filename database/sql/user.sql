
--
-- TABLE: User
-- 
--  

CREATE TABLE User (
  id int unique NOT NULL ,
  name char NOT NULL ,
  mail char NOT NULL ,
  password char NOT NULL 
);

-- 
ALTER TABLE User ADD CONSTRAINT pk_user PRIMARY KEY (id);

CREATE INDEX User_id_index  ON User(id);

CREATE INDEX User_name_index  ON User(name);
ALTER TABLE User ADD CONSTRAINT pk_user_collection_1 FOREIGN KEY (id) REFERENCES CollectionOwnership (user_id);
