# Workspace for TrajDB

## Python API for client interface
* add\_collection(name, ...) - collection\_context
* add\_trajectory(collection, file) - traj\_context (id, new\_name, len, ...) | error (can contain traj ctx of existing traj) 
* append\_trajectory(traj\_context, file) - traj\_context | error
* fetch\_collection(collection\_context) - ...
* search\_collection(pdb, name, length, forcefield, owner, optional\_restrictors)
* remove\_trajectory(traj\_context) - success |error 
* remove\_collection(collection\_context) - success | error

Error handling is performed via exceptions.

### Contexts
The Collection context encapsulates all important fields of collection table and containted trajectory
ids.

A trajectory context contains traj metadata (length, num atoms, reference to topology).
It also contains a backreference to the refering collection (Collection context).

## Database scheme (tables)

* collections(id, name, pdb(+topology), temperature, ...)
* trajectories(id, name, file\_URI, meta data..., coll\_id, parent\_traj\_id) 
* users(id, name, mail, ...)
* collection ownership([collid, userid])

