# TrajDB - a new approach to simulation results sharing

## Purpose 
The main purpose of this database is to make simulation results from molecular
dynamics in form of bundeled trajectory files searchable and downloadable to different working
groups. 

The database holds information about a simulated system like used force fields,
parameters (eg. temperature) and topology to enable people to catalog their
results and optionally share them with others. 

Sharing can be controlled via security tokens, which can be granted
to groups or individuals.

Every participating working group can decide to open their database for the public
or not, since they control their own instance of the service.

The individual data is going to be stored in a working group instance of this
database. This way we avoid uneccessary data duplication and gain a centralized
searchable index for all results produced by a working.

The users can insert their simulation results (trajectories) in the database via
a simple command line interface (CLI) or a web service (RESTful API).

## Features 
In the following sections we are going to describe the functionalities the
service will have.

### upload trajectories
The user can upload individual trajectory files to TrajDB and associate it to
a collection.

Attributes to store:
* uri - where is the trajectory located?
* n\_frame - how long (in frames) is the trajectory?
* timestep - in which interval has the traj been saved?  
* hash - to (re-)identify the file (prior uploading, to avoid duplicates)
* collection - to which collection does this traj belong?

### create collections
A collection holds references to all associated trajectories as well as to the
setup for the simulation.

### create a setup
A setup holds (optionally) all parameters needed to reproduce the results in
principle. Important attributes are:
* topology
* number of atoms
* forcefield
* forcefield parameters
* simulation software (+version)

###   

## Service technical details
To build this API we are using a RESTful
architecture (respresentational state transfer). So the service will have a
uniform interface with a few constraints. One of these is that the resources are
identified in requests (eg. URIs) by the client and interchanged via a common
representation (eg. XML, JSON) 

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

