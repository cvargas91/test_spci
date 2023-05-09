'''
Utiliza las credenciales para crear archivo token.json (necesario para ejecutar script postCreaDirsDrivePOA-ANIO)

Archivo client_secretB.json debe existir en el directorio

Una vez ejecutado el Script, se indicará un link en consola para autenticarse con la cuenta Google.
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

def run():
    django.setup()
    creds = None

    #Eliminar archivo "token.json" para generar uno nuevo según el "client_secret2.json"
    pathToken = 'token.json'
    if os.path.exists(pathToken):
        creds = Credentials.from_authorized_user_file(pathToken, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secretB.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pathToken, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('drive', 'v3', credentials=creds)
        print("Generación Correcta de token.json")
        cont = 0
        
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
