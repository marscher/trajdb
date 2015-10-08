
--
-- TABLE: Group
-- 
--  

CREATE TABLE Group (
  id int NOT NULL ,
  name char NOT NULL ,
  organisation varchar NOT NULL 
);

-- 
ALTER TABLE Group ADD CONSTRAINT pk_g PRIMARY KEY (id);

CREATE INDEX Group_id_index  ON Group(id);

CREATE INDEX Group_name_index  ON Group(name);
