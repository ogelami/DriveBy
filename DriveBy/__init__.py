#!/usr/bin/env python3

import pickle, json, os.path, sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/drive']
config = None

def upload(filename):
  with open('config.json', encoding='utf-8') as json_file:
    config = json.loads(json_file.read())

  creds = None

  if os.path.exists(config['tokenPath']):
    with open(config['tokenPath'], 'rb') as token:
      creds = pickle.load(token)
 
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_config(config['credentials'], SCOPES)

    with open(config['tokenPath'], 'wb') as token:
      pickle.dump(creds, token)

  service = build('drive', 'v3', credentials=creds)

  media = MediaFileUpload(filename, mimetype='application/gzip')
  file_metadata = {'name': filename + datetime.now().strftime("_%Y%m%d_%H%M%S.backup"), 'parents' : [config['destinationFolderId']]}
  response = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

  return response
