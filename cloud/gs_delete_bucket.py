__author__ = 'gumengyuan'

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

print 'FUNCTION: DELETE BUCKET'

#try:
  #oauth2_client.token_exchange_lock = multiprocessing.Manager().Lock()
#except:
  #oauth2_client.token_exchange_lock = threading.Lock()


# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

project_id = 'fabled-tractor-563'

header_values = {"x-goog-project-id": project_id}
uri = boto.storage_uri('', GOOGLE_STORAGE)

# Need to call the list_bucket first to get all buckets, and decide which bucket to delete
for bucket in uri.get_all_buckets(headers=header_values):
    print bucket.name

bucket_name = ""
bucket_name = raw_input("Which bucket would you like to delete: ")

uri = boto.storage_uri(bucket_name, GOOGLE_STORAGE)
for obj in uri.get_bucket():
    print 'Deleting object: %s...' % obj.name
    obj.delete()
print 'Deleting bucket: %s...' % uri.bucket_name
uri.delete_bucket()

