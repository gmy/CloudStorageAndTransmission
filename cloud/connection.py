__author__ = 'gumengyuan'


from boto.s3.connection import S3Connection

s3_access_key = ''
s3_secret_key = ''

def setCredentials(access, secret):
    global s3_access_key
    global s3_secret_key

    s3_access_key = access
    s3_secret_key = secret


def connect():
    try:
        global s3_access_key
        global s3_secret_key

        #print 'access: %s' % s3_access_key
        #print 'secret: %s' % s3_secret_key
        conn = S3Connection(s3_access_key, s3_secret_key)
    except:
        return ''
    else:
        return conn
