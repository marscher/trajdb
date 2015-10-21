## Why Django?
Django is a powerful framework to create full featured web services with support
for several database backends, transparent data handling, tons of available libraries etc.

## Description of services

### Storage
The backend service is a Django application, containing the database backend and
a restful http API to communicate with the service (create new collections, users,
permissions, download data etc.)

Permissions to collections/trajectories will be made via access tokens (grant per
user or group with a certain time limit - will probably be another django app).

If a traj is uploaded, it is being stored systematically (eg. collection/ folder)  in a central pool.

If a traj already is on the same filesystem we should avoid a copy, and do a move instead.
This can be achieved via associated URI analysis.

### Download service
Since files are being stored in a central repo associated to the backend instance,
it is possible to download all files from there.

The protocol should support resuming downloads (HTTP is capable of doing so - impl in client app).

#### URI

The unified resource identifier associated with each trajectory can look like this:

trajdb://instance:port/collection/trajname

The service translates this into a file:/// uri and presents this via the web-server
to the client who requested the download.


## Technical features
* RESTful webservice API via:
  * https://django-tastypie.readthedocs.org/en/latest/ or
  * http://www.django-rest-framework.org/

* token based access to trajectory files (if desired) via
  https://pypi.python.org/pypi/django-access-tokens


