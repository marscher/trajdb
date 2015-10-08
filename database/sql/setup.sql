
--
-- TABLE: Setup
-- 
--  

CREATE TABLE Setup (
  id int NOT NULL ,
  description varchar(255) NOT NULL ,
  pdb char(4) NOT NULL ,
  program varchar NOT NULL ,
  program_version varchar NOT NULL ,
  topology varbinary NOT NULL ,
  topology_type varchar NOT NULL ,
  forcefield_name varchar NOT NULL ,
  forcefield_parameters varbinary NOT NULL ,
  forcefield_parameters_type varchar NOT NULL 
);

-- 
ALTER TABLE Setup ADD CONSTRAINT pk_setups PRIMARY KEY (id);

CREATE INDEX Setup_id_index  ON Setup(id);

CREATE INDEX Setup_pdb_index  ON Setup(pdb);

CREATE INDEX Setup_program_index  ON Setup(program);
ALTER TABLE Setup ADD CONSTRAINT  FOREIGN KEY () REFERENCES Collection ();
