
--
-- TABLE: GroupMembership
-- 
--  

CREATE TABLE GroupMembership (
  group_id int NOT NULL ,
  user_id int NOT NULL 
);

-- 
ALTER TABLE GroupMembership ADD CONSTRAINT pk_groupmembership PRIMARY KEY (group_id,user_id);
ALTER TABLE GroupMembership ADD CONSTRAINT  FOREIGN KEY () REFERENCES User ();
ALTER TABLE GroupMembership ADD CONSTRAINT  FOREIGN KEY () REFERENCES User ();
ALTER TABLE GroupMembership ADD CONSTRAINT fk_group FOREIGN KEY (group_id) REFERENCES Group (id);
ALTER TABLE GroupMembership ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES User (id);
