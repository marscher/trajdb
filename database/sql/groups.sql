
--
-- TABLE: Groups
-- 
--  

CREATE TABLE Groups (
  id int NOT NULL ,
  name char NOT NULL ,
  organisation varchar(255) NOT NULL 
);

-- 
ALTER TABLE Groups ADD CONSTRAINT pk_group PRIMARY KEY (id);

CREATE INDEX Groups_id_index  ON Groups(id);

CREATE INDEX Groups_name_index  ON Groups(name);
