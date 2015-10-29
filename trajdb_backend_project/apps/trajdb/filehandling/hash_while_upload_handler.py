'''
Created on 21.10.2015

@author: marscher
'''

from django.core.files.uploadhandler import TemporaryFileUploadHandler
import hashlib


class HashWhileWriteUploadHandler(TemporaryFileUploadHandler):

    def __init__(self, *args, **kw):
        super(HashWhileWriteUploadHandler, self).__init__(*args, **kw)

        self._hash_func = hashlib.sha512()
        self.hash = None

    def receive_data_chunk(self, raw_data, start):
        # write the chunk
        TemporaryFileUploadHandler.receive_data_chunk(self, raw_data, start)

        # hash the chunk
        self._hash_func.update(raw_data)

    def file_complete(self, file_size):
        self.hash = self._hash_func.hexdigest()
        print ("file upload compelete: hash=%s" % self.hash)
        return TemporaryFileUploadHandler.file_complete(self, file_size)
