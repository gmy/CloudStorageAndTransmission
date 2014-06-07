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

def delete():
    print 'FUNCTION: DELETE BUCKET'

    try:
        oauth2_client.token_exchange_lock = multiprocessing.Manager().Lock()
    except:
        oauth2_client.token_exchange_lock = threading.Lock()


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
    bucket_name = raw_input("Which bucket would you like to enter: ")

    uri = boto.storage_uri(bucket_name, GOOGLE_STORAGE)
    print 'Objects in %s are listed below: ' % bucket_name
    for obj in uri.get_bucket():
        print '%s://%s/%s' % (uri.scheme, uri.bucket_name, obj.name)

    object_name = ""
    object_name = raw_input("Which object would you like to delete: ")
    uri = boto.storage_uri(bucket_name+'/'+object_name, GOOGLE_STORAGE)

    uri.delete_key()