
--
-- TABLE: Trajectory
-- stores trajectory files in a collection.
-- Can reference its parent in case of adaptive sampling
--  

CREATE TABLE Trajectory (
  id int NOT NULL ,
  name char(255) NOT NULL ,
  parent_traj_id int,
  collection_id int NOT NULL ,
  uri varchar(1000) NOT NULL 
);

-- 
ALTER TABLE Trajectory ADD CONSTRAINT pk_trajectories PRIMARY KEY (id);

-- 
ALTER TABLE Trajectory ADD CONSTRAINT fk_parent_traj FOREIGN KEY (parent_traj_id) REFERENCES Trajectory(id) ON UPDATE NO ACTION ON DELETE NO ACTION;

-- 
ALTER TABLE Trajectory ADD CONSTRAINT fk_traj_in_collection FOREIGN KEY (collection_id) REFERENCES Collection(id) ON UPDATE NO ACTION ON DELETE NO ACTION;

CREATE INDEX Trajectory_id_index  ON Trajectory(id);
ALTER TABLE Trajectory ADD CONSTRAINT fk_traj_collection FOREIGN KEY (collection_id) REFERENCES Collection (id);
