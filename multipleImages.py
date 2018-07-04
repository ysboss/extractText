"""
Shows basic usage of the Drive v3 API.

Creates a Drive v3 API service and prints the names and ids of the last 10 files
the user has access to.
"""

from __future__ import print_function
import os, time

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload
from apiclient import discovery

start_time = time.time()

# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive.file'
#SCOPES = 'https://www.googleapis.com/drive/v3/files'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
drive = build('drive', 'v3', http=creds.authorize(Http()))

# Get folder id
folder_id = '1TsBBBp91A9DGmE6nLSkWy78oIZVJqwsF'
mimeType = 'application/vnd.google-apps.document'

files = os.listdir('testimages')

for filename in files:
    body = {'name': filename,
            'parents': [folder_id],
            'mimeType': mimeType
        }

    res = drive.files().create(body=body, media_body='testimages/'+filename).execute()
    if res:
        print ('Upload "%s"' % (res['name']))

        MIMETYPE='text/plain'
        data = drive.files().export(fileId=res['id'], mimeType = MIMETYPE).execute()
        if data:
            fn = '%s.txt' % os.path.splitext(filename)[0]
            with open('results/'+fn, 'wb') as fh:
                fh.write(data)
            print ('Downloaded "%s" ' % (fn))
            #print("------%s seconds ---------" % (time.time()-start_time))


print("---------------------%s seconds -------------------" % (time.time()-start_time))



# file_metadata = {
#     'name': 'photo.jpg',
#     'parents': [folder_id],
#     'mimeType': 'application/vnd.google-apps.document'
# }
#
# media = MediaFileUpload('IMG_3136.JPG',
#                         mimetype='image/jpeg',
#                         resumable=True)
#
# file = drive.files().create(body=file_metadata,
#                                     media_body=media,
#                                     fields='id').execute()
# print ('File ID: %s' % file.get('id'))

# file_metadata = {
#     ('IMG_3011.JPG', 'application/vnd.google-apps.document'),
#     ('IMG_3136.JPG', 'application/vnd.google-apps.document'),
#     ('IMG_1932.JPG', 'application/vnd.google-apps.document'),
#     ('IMG_1478.JPG', 'application/vnd.google-apps.document'),
#     ('IMG_1464.JPG', 'application/vnd.google-apps.document'),
# }


# file_metadata = {
#      'name': 'my',
#      'mimeType': 'application/vnd.google-apps.document'
# }
#
# media = MediaFileUpload('IMG_3011.JPG',
#                         mimetype='image/jpeg'
#                         )
# file = drive.files().create(body=file_metadata,
#                                     media_body=media,
#                                     fields='id').execute()
# print ('File ID: %s' % file.get('id'))










# Call the Drive v3 API
# results = service.files().list(
#     pageSize=10, fields="nextPageToken, files(id, name)").execute()
# items = results.get('files', [])
# if not items:
#     print('No files found.')
# else:
#     print('Files:')
#     for item in items:
#         print('{0} ({1})'.format(item['name'], item['id']))
