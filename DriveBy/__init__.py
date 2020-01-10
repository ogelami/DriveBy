#!/usr/bin/env python3

import pickle, json, os, sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from datetime import datetime

service = None
config = None
configurationPath = os.environ['DRIVEBY_CONFIG_PATH'] if 'DRIVEBY_CONFIG_PATH' in os.environ else '/etc/driveby/config.json'

def init():
  global config
  SCOPES = ['https://www.googleapis.com/auth/drive']

  with open(configurationPath, encoding='utf-8') as json_file:
    config = json.loads(json_file.read())

  os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['serviceAccountSecretPath']

  creds = None

  if os.path.exists(config['tokenPath']):
    with open(config['tokenPath'], 'rb') as token:
      creds = pickle.load(token)
 
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(config['clientSecretPath'], SCOPES)

    with open(config['tokenPath'], 'wb') as token:
      pickle.dump(creds, token)

  return build('drive', 'v3', credentials=creds)

def backup(filename):
  media = MediaFileUpload(filename, mimetype='application/gzip')
  file_metadata = {'name': filename + datetime.now().strftime("_%Y%m%d_%H%M%S.backup")}

  if config['parentFolderId']:
    file_metadata['parents'] = [config['parentFolderId']]

  response = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

  return response

def dump():
  results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()
  items = results.get('files', [])

  if not items:
    print('No files found.')
  else:
    print('Files:')
    for item in items:
      print(u'{0} ({1})'.format(item['name'], item['id']))

def delete(filename):
  return

service = init()
