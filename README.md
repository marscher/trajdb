# TrajDB - a new approach to simulation results sharing

## Purpose 
The main purpose of this database is to make simulation results from molecular
dynamics in form of bundled trajectory files search-able and downloadable to different working
groups. 

The database holds information about a simulated system like used force fields,
parameters (eg. temperature) and topology to enable people to catalog their
results and optionally share them with others. 

Sharing can be controlled via security tokens, which can be granted
to groups or individuals.

Every participating working group can decide to open their database for the public
or not, since they control their own instance of the service.

The individual data is going to be stored in a working group instance of this
database. This way we avoid unnecessary data duplication and gain a centralized
searchable index for all results produced by a working.

The users can insert their simulation results (trajectories) in the database via
a simple command line interface (CLI) or a web service (RESTful API).

The user may hold a local instance of the database for offline working and
synchronization purposes.


## Features 
In the following sections we are going to describe the functionalities the
service will have.

During the registration and upload process of the data the user has to create
a 'setup' entry, which describes how the simulation has been parametrized.
The setup entry is then being associated to a collection, which then finally holds
the individual trajectory entries.

If a collection already exists the trajectories can directly be added to it.

### create a setup
A setup holds (optionally) all parameters needed to reproduce the results in
principle.

Important attributes are:

* topology - this field may contain a blob (and if so an additional column with its type, to interpret the data) 
* number of atoms
* a reference pdb (optional)
* force-field
* force-field parameters
* simulation software (+version)
* script - an optional script to run a simulation
* owner - reference to user profile

### create collections
A collection holds references to all associated trajectories as well as to the
setup for the simulation.

Attributes to store:

* name - a short name
* description - a brief description of the collection.
* owner - refers to a user profile on the server.
* cumulative length - sum of all trajectories in collection (physical time unit). 
* number of atoms/particles - actually stored in the setup..., but here for performance reasons?
* setup - reference to a setup entry \ how has this data been generated? 
* created - timestamp when this collection has been created.

### meta-collections?
A collection can be part in multiple meta-collection which helps to catalog
even more. A meta-collection can also be part of other meta-collections. This
way we can build hierarchies of collections.

### upload trajectories
The user can upload individual trajectory files to TrajDB and associate it to
a collection. The decision to which collection the file is being added to has
to be maden prior uploading to avoid loose files.

Attributes to store:

* uri - where is the trajectory located? (in-case of multiple data stores)
* n\_frame - how long (in frames) is the trajectory?
* timestep - in which interval has the traj been saved?  
* hash - to (re-)identify the file (prior uploading, to avoid duplicates) and
  to verify downloaded files.
* collection - to which collection does this traj belong? Every traj needs to
  have at least one collection.
* created - timestamp when this traj has been created/uploaded.
* reference to parent trajectory - if this traj has been "forked" from another
  traj, remember this "inheritance". Optional 
* parent traj frame - index of the parent trajs frame. Optional 

### download collection/trajectory
By specifying the id of a data set the client selects which data he or she wants.
The server will then answer with a list of URIs, from which the data can be
downloaded. 

Downloads support resuming in case of interruption. Downloaded files can be validated
with the stored hash value to avoid data corruption.

Streaming the file(s) directly (recommended for data store on network file system)
to the client shall be possible. This avoids unnecessary copies.

### extend trajectory
There exists a trajectory entry with the same setup in the data base which 
needs to be prolonged. The user has to specify which trajectory will be 
extended and provides the data. The service ensures that only compatible
trajectories can be concatenated (eg. by checking the topology and the difference
of coordinates).

After the submission of the fragment and its validation the server concatenates
the files in its data store.

## Service technical details
To build this API we are using a RESTful architecture (respresentational state
transfer). So the service will have a uniform interface with a few constraints.
One of these is that the resources are identified in requests (eg. URIs) by the
client and interchanged via a common representation (eg. XML, JSON).

Every entity of the service (like trajectory, collection or setup) has a
dictionary like structure which can bre requested by the API of the service.
There is the possibility to request a HTML view of the data to directly obtain
a human readable representation.

So if the user accesses a collection under http://service/collection/id
he or she will get a JSON dictionary containing all the important attributes
and hyperlinks to contained trajectory entities in the form of
http://service/traj/id

There are also list views available for setups and collections.

### uploading files
If the file lies on the same (network) file system as the data store, we want to
avoid passing the file through an extra service, but just make a copy. This is
a common use case in local networks.

Client has to provide some kind of "source" information of the file, the server
then decides if the file needs to be uploaded or copied.

In case of NFS this could be done via the fsid attribute of the NFS filesystem.

Protocol decision? 
HTTP server would have to allow very large POST requests, which is not desirable.

Alternatives:

* FTP - eg. Django-ftpserver, create a temporary account for the upload session.
  Move the uploaded files to the data store on the server side.
* ...

### Python API for client interface
* add\_collection(name, ...) - collection\_context
* add\_trajectory(collection, file) - traj\_context (id, new\_name, len, ...) | error (can contain traj ctx of existing traj) 
* append\_trajectory(traj\_context, file) - traj\_context | error
* fetch\_collection(collection\_context) - ...
* search\_collection(pdb, name, length, forcefield, owner, optional\_restrictors)
* remove\_trajectory(traj\_context) - success |error 
* remove\_collection(collection\_context) - success | error

Error handling is performed via exceptions.

#### Contexts
The Collection context encapsulates all important fields of collection table
and contained trajectory ids.

A trajectory context contains traj metadata (length, num atoms, reference to topology).
It also contains a back-reference to the referring collection (Collection context).

The data-structure used here shall be an ordinary Python dictionary, so we can
easily exchange those structures via JSON serialization.

### Database scheme (tables)

* collections(id, name, pdb(+topology), temperature, ...)
* trajectories(id, name, file\_URI, meta data..., coll\_id, parent\_traj\_id) 
* users(id, name, mail, ...)
* collection ownership([collid, userid])


