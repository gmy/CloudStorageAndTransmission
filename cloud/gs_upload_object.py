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

def upload():
    print 'FUNCTION: UPLOAD OBJECT'
    print ''

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

    ### CALL GS_LIST_BUCKET HERE
    for bucket in uri.get_all_buckets(headers=header_values):
        print bucket.name
    ###

    bucket_name = ""
    bucket_name = raw_input("Please choose the bucket to upload the object: ")
    dir = ""
    dir = raw_input("Select your directory: ")
    filename = ""
    filename = raw_input("Select your uploading file: ")

    with open(os.path.join(dir, filename), 'r') as localfile:
        dst_uri = boto.storage_uri(
            bucket_name + '/' + filename, GOOGLE_STORAGE)
        dst_uri.new_key().set_contents_from_file(localfile)
    print 'Successfully created "%s/%s"' % (
        dst_uri.bucket_name, dst_uri.object_name)