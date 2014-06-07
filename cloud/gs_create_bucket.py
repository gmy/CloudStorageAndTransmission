__author__ = 'gumengyuan'
#!/usr/bin/python

import boto
import multiprocessing
import os
import shutil
import StringIO
import tempfile
import threading
import time
from gslib.third_party.oauth2_plugin import oauth2_plugin
from gslib.third_party.oauth2_plugin import oauth2_client

def create():
        print 'FUNCTION: CREATE BUCKET'

        try:
            oauth2_client.token_exchange_lock = multiprocessing.Manager().Lock()
        except:
            oauth2_client.token_exchange_lock = threading.Lock()

        #token = oauth2_client.InMemoryTokenCache()
        #access_key = oauth2_client.InMemoryTokenCache.GetToken(token, 'client_secret')
        #print '%s',access_key
        # URI scheme for Google Cloud Storage.
        GOOGLE_STORAGE = 'gs'
        # URI scheme for accessing local files.
        LOCAL_FILE = 'file'

        project_id = 'fabled-tractor-563'

        ###########BUCKET NAME REQUIREMENT############
        #Bucket names must contain only lowercase letters, numbers, dashes (-), underscores (_), and dots (.). Names containing dots require verification.
        #Bucket names must start and end with a number or letter.
        #Bucket names must contain 3 to 63 characters. Names containing dots can contain up to 222 characters, but each dot-separated component can be no longer than 63 characters.
        #Bucket names cannot be represented as an IP address in dotted-decimal notation (for example, 192.168.5.4).
        #Bucket names cannot begin with the "goog" prefix.
        ##############################################
        bucket_name = ""
        bucket_name = raw_input("What would you like to name your bucket: ")

        # Instantiate a BucketStorageUri object.
        uri = boto.storage_uri(bucket_name, GOOGLE_STORAGE)

        try:
            header_values = {"x-goog-project-id": project_id}
            uri.create_bucket(headers=header_values)

            print 'Successfully created bucket "%s"' % bucket_name
        except boto.exception.StorageCreateError, e:
            print 'Failed to create bucket:', e
