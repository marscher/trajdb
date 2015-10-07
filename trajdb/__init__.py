""" API draft for trajDB
"""

class CollectionContext(object):
    name = None
    pdb = None
    forcefield = None
    owner = None
    length = None

class TrajectoryContext(object):
    uri = None
    collection_ctx = None
    file_name = None
 
def add_collection(name, *args):
    pass

def add_trajectory(collection_ctx, file_name):
    pass

def append_trajectory(trajectory_ctx, file_name):
    pass

def search_collection(name=None, pdb=None, length=None, forcefield=None,
                      owner=None, restrictor=None):
    pass

def fetch_collection(collection_ctx):
    pass

def remove_trajectory(traj_ctx):
    pass

def remove_collection(collection_ctx):
    pass

