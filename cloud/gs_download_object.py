__author__ = 'gumengyuan'

import boto
import multiprocessing
import os
import shutil
import StringIO
import tempfile
import threading
import time
import urllib2
from gslib.third_party.oauth2_plugin import oauth2_plugin
from gslib.third_party.oauth2_plugin import oauth2_client

def download():
    print 'FUNCTION: DOWNLOAD OBJECT'
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

    ### CALL GS_LIST_OBJECT FIRST
    print 'All buckets are listed below: '
    for bucket in uri.get_all_buckets(headers=header_values):
        print bucket.name
    print ''

    bucket_name = ""
    bucket_name = raw_input("Please select the bucket first: ")
    uri = boto.storage_uri(bucket_name, GOOGLE_STORAGE)
    print 'Objects in %s are listed below: ' % (bucket_name)
    for obj in uri.get_bucket():
        print '%s://%s/%s' % (uri.scheme, uri.bucket_name, obj.name)
    ###

    filename = ""
    filename = raw_input("Which file to download: ")
    dest_dir = ""
    dest_dir = raw_input("Input the downloading directory: ")
    src_uri = boto.storage_uri(bucket_name + '/' + filename, GOOGLE_STORAGE)

    # Create a file-like object for holding the object contents.
    object_contents = StringIO.StringIO()

    # The unintuitively-named get_file() doesn't return the object
    # contents; instead, it actually writes the contents to
    # object_contents.
    src_uri.get_key().get_file(object_contents)

    dst_uri = boto.storage_uri(os.path.join(dest_dir, filename), LOCAL_FILE)
    object_contents.seek(0)
    dst_uri.new_key().set_contents_from_file(object_contents)

    object_contents.close()

