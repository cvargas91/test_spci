'''
Crea la estructura de directorios en Google Drive
'''

import django
import os.path
from webapp.models import *

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def callback(request_id, response, exception):
    if exception:
        # Handle error
        print(exception)
    else:
        print("Permission Id: {}".format(response.get('id')))

def run():
    django.setup()
    creds = None
    pathToken = 'token.json'
    if os.path.exists(pathToken):
        creds = Credentials.from_authorized_user_file(pathToken, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret2.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pathToken, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('drive', 'v3', credentials=creds)
        file_id = '1Q-mDOiOwO1kY4nfxWiwfSwoygMHTUzje'

        batch = service.new_batch_http_request(callback=callback)
        user_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': 'gitlab@uaysen.cl'
        }
        batch.add(service.permissions().create(
                fileId=file_id,
                body=user_permission,
                fields='id',
                sendNotificationEmail=False
        ))
        batch.execute()

        'commenter'
        '''
        for accion in Accion.objects.all() :
            print(accion.dirGoogle)
        '''
            
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
