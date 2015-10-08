
--
-- TABLE: Collection
-- 
--  

CREATE TABLE Collection (
  id int NOT NULL ,
  name char(255) NOT NULL ,
  description varchar(255) NOT NULL ,
  length int unsigned NOT NULL  DEFAULT 0,
  n_atoms int unsigned NOT NULL , -- number of atoms
  setup_id int NOT NULL 
);

-- 
ALTER TABLE Collection ADD CONSTRAINT pk_collection PRIMARY KEY (id);

-- 
ALTER TABLE Collection ADD CONSTRAINT fk_setup FOREIGN KEY (setup_id) REFERENCES Setup(id) ON UPDATE NO ACTION ON DELETE NO ACTION;

CREATE INDEX Collection_id_index  ON Collection(id);

CREATE INDEX Collection_name_index  ON Collection(name);
ALTER TABLE Collection ADD CONSTRAINT fk_collection_ownership FOREIGN KEY (id) REFERENCES CollectionOwnership (collection_id);
ALTER TABLE Collection ADD CONSTRAINT fk_setup FOREIGN KEY (setup_id) REFERENCES Setup (id);
