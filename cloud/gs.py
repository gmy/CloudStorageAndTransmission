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
import connection
from gslib.third_party.oauth2_plugin import oauth2_plugin
from gslib.third_party.oauth2_plugin import oauth2_client
from cs import CSOperations

try:
    oauth2_client.token_exchange_lock = multiprocessing.Manager().Lock()
except:
    oauth2_client.token_exchange_lock = threading.Lock()

GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'
project_id = 'fabled-tractor-563'

# gs_access_key_id = '520372840160-mmu8ulk7s1qbr5k3g15bmes0j3mga7pu.apps.googleusercontent.com'
# gs_secret_access_key = 'HG9uFNSmr-Nim_lMgbN-EWYR'
# conn = boto.connect_gs(gs_access_key_id,gs_secret_access_key)

class GSOperations(CSOperations):
    @staticmethod
    def make_bucket(bucket_name):
        print 'FUNCTION: MAKE BUCKET'
        print ''
        #bucket_name = raw_input("What would you like to name your bucket: ")

        if len(bucket_name) == 0:
            return 'Bucket name cannot be empty'
        # Instantiate a BucketStorageUri object.
        uri = boto.storage_uri(bucket_name, GOOGLE_STORAGE)

        try:
            header_values = {"x-goog-project-id": project_id}
            uri.create_bucket(headers=header_values)
            #mybucket = conn.create_bucket(bucket_name)
        except boto.exception.StorageCreateError, e:
            print 'Sorry, but failed to create bucket!'
            return 'Failed to create a new bucket! Please check the name. It should be unique within GS naming space.'
        else:
            print 'Successfully created bucket "%s"' % bucket_name
            return 'Successfully created bucket "%s"' % bucket_name

    @staticmethod
    def list_bucket():
        print 'FUNCTION: LIST BUCKET'
        print ''

        header_values = {"x-goog-project-id": project_id}
        uri = boto.storage_uri('', GOOGLE_STORAGE)
        try:
            buckets = []
            for bucket in uri.get_all_buckets(headers=header_values):
                buckets.append(bucket)
                #buckets = conn.get_all_buckets()
            return buckets
        except:
            return []

    @staticmethod
    def remove_bucket(bucket):
        print 'FUNCTION: DELETE BUCKET'
        print ''

        # header_values = {"x-goog-project-id": project_id}
        # uri = boto.storage_uri('', GOOGLE_STORAGE)

        # Need to call the list_bucket first to get all buckets, and decide which bucket to delete
        #for bucket in uri.get_all_buckets(headers=header_values):
            #print bucket.name
        #self.list_bucket()

        #bucket_name = ""
        bucket_name = bucket.name #raw_input("Which bucket would you like to delete: ")

        uri = boto.storage_uri(bucket_name, GOOGLE_STORAGE)


        for obj in uri.get_bucket():
            print 'Deleting object: %s...' % obj.name
            obj.delete()
        print 'Deleting bucket: %s...' % uri.bucket_name
        uri.delete_bucket()
        # except:
        #     return 'Fail to delete bucket %s!' % uri.bucket_name
        # else:
        #     return 'Successfully delete bucket %s!' % uri.bucket_name

    @staticmethod
    def list_object(bucket):
        print 'FUNCTION: LIST OBJECT'
        print ''

        #header_values = {"x-goog-project-id": project_id}
        #uri = boto.storage_uri('', GOOGLE_STORAGE)

        # Need to call the list_bucket first to get all buckets, and decide which bucket to list
        #self.list_bucket()

        bucket_name = bucket.name #raw_input("Please select the bucket first: ")
        uri = boto.storage_uri(bucket_name, GOOGLE_STORAGE)
        print 'Objects in %s are listed below: ' % (bucket_name)
        objects = []
        for obj in uri.get_bucket():
            objects.append(obj)
            print '%s://%s/%s' % (uri.scheme, uri.bucket_name, obj.name)
            #list the content of the object
            #print '  "%s"' % obj.get_contents_as_string()

        return objects

    @staticmethod
    def remove_object(bucket, object):
        print 'FUNCTION: DELETE OBJECT'
        print ''

        #header_values = {"x-goog-project-id": project_id}
        #uri = boto.storage_uri('', GOOGLE_STORAGE)

        # Need to call the list_object first to get all buckets, and decide which bucket to delete
        bucket_name = bucket.name

        object_name = object.name #raw_input("Which object would you like to delete: ")
        uri = boto.storage_uri(bucket_name+'/'+object_name, GOOGLE_STORAGE)

        uri.delete_key()
        # except:
        #     msg = 'Fail to remove object %s.', object.name
        #     return msg
        # else:
        #     msg = 'Successfully remove the object %s.', object.name
        #     return msg


    @staticmethod
    def upload_object(bucket, dir, filename):
        print 'FUNCTION: UPLOAD OBJECT'
        print ''

        # Call list_bucket first
        #self.list_bucket()

        bucket_name = bucket.name #raw_input("Please choose the bucket to upload the object: ")
        #dir = raw_input("Select your directory: ")
        #filename = raw_input("Select your uploading file: ")

        try:
            with open(os.path.join(dir, filename), 'r') as localfile:
                dst_uri = boto.storage_uri(
                    bucket_name + '/' + filename, GOOGLE_STORAGE)
                dst_uri.new_key().set_contents_from_file(localfile)
        except:
            msg = 'Sorry, but fail to upload file: "%s".' % filename
            return msg
        else:
            msg = 'Successfully created "%s" in bucket %s!' % (
                dst_uri.object_name, dst_uri.bucket_name)
            return msg

    @staticmethod
    def download_object(bucket, filename, dest_dir):
        print 'FUNCTION: DOWNLOAD OBJECT'
        print ''

        # Call list_object first
        bucket_name = bucket.name #self.list_object()

        #filename = raw_input("Which file to download: ")
        #dest_dir = raw_input("Input the downloading directory: ")
        src_uri = boto.storage_uri(bucket_name + '/' + filename, GOOGLE_STORAGE)

        # Create a file-like object for holding the object contents.
        object_contents = StringIO.StringIO()

        # The unintuitively-named get_file() doesn't return the object
        # contents; instead, it actually writes the contents to
        # object_contents.
        try:
            src_uri.get_key().get_file(object_contents)

            dst_uri = boto.storage_uri(os.path.join(dest_dir, filename), LOCAL_FILE)
            object_contents.seek(0)
            dst_uri.new_key().set_contents_from_file(object_contents)

            object_contents.close()
        except:
            msg = 'Sorry, but fail to download file: "%s".' % filename
            return msg
        else:
            msg = 'Successfully downloaded "%s"!' % filename
            return msg


    @staticmethod
    def move_object(bucket_from, bucket_to, file):
        print 'FUNCTION: MOVE OBJECT'
        print ''

        # Call list_object first
        bucket_from_name = bucket_from.name #self.list_object()

        #filename = raw_input("Which file to download: ")
        #dest_dir = raw_input("Input the downloading directory: ")
        src_uri = boto.storage_uri(bucket_from_name + '/' + file.name, GOOGLE_STORAGE)

        # Create a file-like object for holding the object contents.
        object_contents = StringIO.StringIO()

        try:
            src_uri.get_key().get_file(object_contents)

            conn = connection.connect()
            bucket = conn.get_bucket(bucket_to.name)
            key = bucket.new_key(file.name)
            object_contents.seek(0)
            key.set_contents_from_file(object_contents)

            object_contents.close()
        except:
            msg = 'Sorry, but fail to move file: "%s".' % file.name
            return msg
        else:
            msg = 'Successfully move "%s"!' % file.name
            return msg
