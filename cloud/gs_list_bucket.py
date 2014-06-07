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

def list():
    print 'FUNCTION: LIST BUCKET'
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

    for bucket in uri.get_all_buckets(headers=header_values):
        print bucket.name