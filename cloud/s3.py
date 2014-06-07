__author__ = 'gumengyuan'

import os.path
import boto
import sys
import os
import StringIO
import connection
from cs import CSOperations




# keys = loadCredentials()
# access_key = ''
# secret_key = ''
# conn = ''
# if keys != []:
#     access_key = keys[0]
#     secret_key = keys[1]
#     conn =
# print access_key
# print secret_key

class S3Operations:

    @staticmethod
    def make_bucket(bucket_name):
        conn = connection.connect()
        try:
            bucket = conn.create_bucket(str(bucket_name).lower())
        except boto.exception.S3CreateError:
            msg = "There is a bucket with the same Name. Please Try again!"
            print msg
            return msg
        else:
            msg = "Bucket created successfully!"
            print msg
            return msg

    @staticmethod
    def list_bucket():
        #conn = boto.connect_s3()
        conn = connection.connect()
        allBuckets = conn.get_all_buckets()
        if len(allBuckets) == 0:
 			return "You have No buckets yet!"
        else:
            buckets = []

            for b in allBuckets:
                print b.name
                buckets.append(b)
            return buckets

    @staticmethod
    def remove_bucket(bucket):
        #conn = boto.connect_s3()
        conn = connection.connect()
        toBeDeletedBucket=str(bucket.name.lower())
        #First we need to check if there is a bucket of the same name or it is not found
        try:
            nonexistent = conn.lookup(toBeDeletedBucket)
            if nonexistent is None:
                return "No such bucket!"
            else:
            #No need to validate we alreday checked its existence
                print "Caution: If the bucket is Full, all its contents will be ERASED! "
                #proceed = raw_input('Are you sure you want to proceed yes/no ?')
                #full_bucket = None
                #if (proceed == 'yes'):
                full_bucket = conn.get_bucket(toBeDeletedBucket, validate=False)
                    # It's full of keys. Delete them all.
                for key in full_bucket.list():
                    key.delete()
                    # The bucket is empty now. Delete it.
                conn.delete_bucket(toBeDeletedBucket)
                #else:
                    #print "Delete Bucket Operation Aborted!"
            return "Bucket deletion successful!"
        except:
            return "Failed to delete bucket."


    @staticmethod
    def list_object(bucket):
        #conn = boto.connect_s3()
        conn = connection.connect()
        bucketName=str(bucket.name.lower())

        nonexistent = conn.lookup(bucketName)
        objects = []
        if nonexistent is None:
            print "No such bucket!"
        else:

            mybucket = conn.get_bucket(bucketName)
            for key in mybucket.list():
                print "{name}\t{size}\t{modified}".format(
                    name = key.name,
                    size = key.size,
                    modified = key.last_modified,
                )
                objects.append(key)
        return objects

    @staticmethod
    def remove_object(bucket, object):
        try:
            #conn = boto.connect_s3()
            conn = connection.connect()
            bucketNameSlashPath=str(bucket.name.lower())
            toBeDeletedFileName=str(object.name)

            #seperate bucket name from the path
            listOfStrings=bucketNameSlashPath.split('/', 1)
            numberOfStrings=len(listOfStrings)
            bucketName=listOfStrings[0]
            if(numberOfStrings==2):
                path=listOfStrings[1]
            else:
                path=''


            b = conn.get_bucket(bucketName)
            from boto.s3.key import Key
            # It's full of keys. Delete them all
            full_key_name = os.path.join(path, toBeDeletedFileName)
            k = Key(b)
            k.key = full_key_name
            k.delete()
            return "Successfully delete the file!"

        except:
            return "Object Deletion Failed."



    @staticmethod
    def upload_object(bucket, localDirectory, filename):
    #takes a bucketname/path as a first parameter and
    #a local fileName as a second parameter and uploads it to S3
        try:
            #conn = boto.connect_s3()
            conn = connection.connect()
            bucketNameSlashPath=str(bucket.name)
            localDir= str(localDirectory)
            localFileName=str(filename)

            #seperate bucket name from the path
            listOfStrings=bucketNameSlashPath.split('/', 1)
            numberOfStrings=len(listOfStrings)
            bucketName=listOfStrings[0]
            if(numberOfStrings==2):
                path=listOfStrings[1]
            else:
                path=''


            full_key_name = os.path.join(path, localFileName)
            #need to extract the buffer name from the input string
            bucket = conn.get_bucket(bucketName)
            key = bucket.new_key(full_key_name)
            fullLocalFileName= os.path.join(localDir, localFileName)
            print fullLocalFileName
            key.set_contents_from_filename(fullLocalFileName)
            return "Upload Successful"

        except:
            return "Upload Failed"

    @staticmethod
    def download_object(bucket, filename, dest_dir):
        #takes a bucketname/path/ as a first parameter and
        #a local fileName as a second parameter and downloads it to local pc
        try:
            #conn = boto.connect_s3()
            conn = connection.connect()
            bucketNameSlashPath=str(bucket.name.lower())
            localDir= str(dest_dir)
            localFileName=str(filename)


            #seperate bucket name from the path
            listOfStrings=bucketNameSlashPath.split('/', 1)
            numberOfStrings=len(listOfStrings)
            bucketName=listOfStrings[0]
            if(numberOfStrings==2):
                path=listOfStrings[1]
            else:
                path=''


            full_key_name = os.path.join(path, localFileName)
            print full_key_name
            #need to extract the buffer name from the input string
            from boto.s3.key import Key
            bucket = conn.get_bucket(bucketName)
            mylist=bucket.list()

            #for b in mylist:
            #  print b.name
            k = Key(bucket)
            k.key = full_key_name
            fullLocalFileName= os.path.join(localDir, localFileName)
            print fullLocalFileName
            k.get_contents_to_filename(fullLocalFileName)
            return "Download Successful."
        except:
            return "Download Failed."

    @staticmethod
    def move_object(bucket_from, bucket_to, file):
        conn = connection.connect()
        bucket_from_name = bucket_from.name #self.list_object()


        #src_uri = boto.storage_uri(bucket_from_name + '/' + file.name, 'gs')

        # Create a file-like object for holding the object contents.
        object_contents = StringIO.StringIO()

        try:
            from boto.s3.key import Key
            k = Key(bucket_from)
            k.key = file.name
            #k.key.get_file(object_contents)
            k.get_contents_to_file(object_contents)

            dst_uri = boto.storage_uri(
                    bucket_to.name + '/' + file.name, 'gs')
            object_contents.seek(0)
            dst_uri.new_key().set_contents_from_file(object_contents)

            # bucket = conn.get_bucket(bucket_to.name)
            # key = bucket.new_key(file.name)
            #
            # key.set_contents_from_file(object_contents)

            object_contents.close()
        except:
            msg = 'Sorry, but fail to move file: "%s".' % file.name
            return msg
        else:
            msg = 'Successfully move "%s"!' % file.name
            return msg