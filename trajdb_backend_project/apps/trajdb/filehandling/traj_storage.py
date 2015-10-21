'''
Created on 20.10.2015

@author: marscher
'''

from django.core.files.storage import FileSystemStorage

class TrajStorage(FileSystemStorage):
    pass
#     '''
#     classdocs
#     '''
# 
#     def __init__(self, location):
#         self.location = location
# 
#     def put(self, traj, sha512sum):
#         assert len(sha512sum) == 128
#         pass
#         # move the traj to location
# 
#         # validate the hash, raise in case of errors
# 
#     def get(self, hash):
#         # hashes are primary keys?
#         pass
