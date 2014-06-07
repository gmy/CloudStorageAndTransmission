__author__ = 'gumengyuan'

import sys
from oauth2client.client import flow_from_clientsecrets
from oauth2client import tools

def downloadUsage(err, downloadUrl=None):
  """Emit usage statement with download information."""
  if downloadUrl is None:
    downloadString = 'Run'
  else:
    downloadString = 'Download available at %s or run' % downloadUrl
  print '%s\n%s%s' % (
      err,
      downloadString,
      ' setup.py on the google-api-python-client:\n' +
      'https://code.google.com/p/google-api-python-client/downloads')
  sys.exit(1)

def importUsage(lib, downloadUrl=None):
  """Emit a failed import error with download information."""
  downloadUsage('Could not load %s module.' % lib, downloadUrl)


try:
  import gflags
except:
  importUsage('gflags', 'https://code.google.com/p/python-gflags/downloads/')

FLAGS = gflags.FLAGS

try:
  from oauth2client.file import Storage
  from oauth2client.client import OAuth2WebServerFlow
  from oauth2client.tools import run
  import oauth2client
except:
  importUsage('oauth2client')

FLOW = OAuth2WebServerFlow(
    client_id='520372840160-f4t12ku1e3rr14e6lqdsioojrgivue4q.apps.googleusercontent.com',
    client_secret='wkR7gd75pv2l1aYhugUY-AD1',
    redirect_uri='https://melissa.storage.googleapis.com/oauth2callback',
    scope='https://www.googleapis.com/auth/devstorage.full_control',
    user_agent='my-sample/1.0'
)

flow = flow_from_clientsecrets('/Users/gumengyuan/gsutil/client_secrets.json',
                               scope='https://www.googleapis.com/auth/devstorage.full_control',
                               redirect_uri='urn:ietf:wg:oauth:2.0:oob')
#auth_uri = flow.step1_get_authorize_url()
#credentials = flow.step2_exchange("hi")


storage = Storage('/Users/gumengyuan/gsutil/.oauth2.dat')
#credentials = storage.get()
credentials = tools.run_flow(FLOW, storage, FLAGS)