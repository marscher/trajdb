The backend service is a Django application, containing the database backend and
a restful http API to communicate with the service (create new collections, users,
permissions, download data etc.)

Permissions to collections/trajectories will be made via access tokens (grant per
user or group with a certain time limit - will probably be another django app).


## Technical features
* RESTful webservice API via:
  * https://django-tastypie.readthedocs.org/en/latest/ or
  * http://www.django-rest-framework.org/

* token based access to trajectory files (if desired) via
  https://pypi.python.org/pypi/django-access-tokens


