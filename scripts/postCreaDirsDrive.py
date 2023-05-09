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
        idDirBase = '1Yd0TJM1cGFpXlObI9V4F8PbptjmaB110'

        for accion in Accion.objects.filter(origen="PMI") :
            dirAccion = 'ACCION_{}'.format(accion.id_uaysen)
            query = "name='{}' and '{}' in parents".format(dirAccion, idDirBase)
            respuesta = service.files().list(q=query).execute()
            
            # por seguridad, solo se avanza si el dir de la accion no existe 
            if len(respuesta.get('files', [])) == 0 :
                file_metadata = {
                    'name' : 'ACCION_{}'.format(accion.id_uaysen),
                    'mimeType' : 'application/vnd.google-apps.folder',
                    'parents' : [idDirBase]
                }
                file = service.files().create(body=file_metadata, fields='id').execute()
                accion.dirGoogle = file.get('id')
                accion.save()

                # avance pal usuario
                print("accion: {}, dir: {}".format(accion.id_uaysen, accion.dirGoogle))

                file_metadata = {
                    'name' : '{}'.format('MDVs'),
                    'mimeType' : 'application/vnd.google-apps.folder',
                    'parents' : [accion.dirGoogle]
                }
                file = service.files().create(body=file_metadata, fields='id').execute()
                mdvDirId = file.get('id')
                for mdv in accion.mdv_set.all() :
                    file_metadata = {
                        'name' : '{}'.format(mdv.nombre),
                        'mimeType' : 'application/vnd.google-apps.folder',
                        'parents' : [mdvDirId]
                    }
                    file = service.files().create(body=file_metadata, fields='id').execute()
                    mdv.dirGoogle = file.get('id')
                    mdv.save()

                    # avance pal usuario
                    print("mdv, dir: {}".format(mdv.dirGoogle))

                file_metadata = {
                    'name' : '{}'.format('Funciones'),
                    'mimeType' : 'application/vnd.google-apps.folder',
                    'parents' : [accion.dirGoogle]
                }
                file = service.files().create(body=file_metadata, fields='id').execute()
                funcionDirId = file.get('id')
                for funcion in accion.funcion_set.all() :
                    file_metadata = {
                        'name' : '{}'.format(funcion.nombre),
                        'mimeType' : 'application/vnd.google-apps.folder',
                        'parents' : [funcionDirId]
                    }
                    file = service.files().create(body=file_metadata, fields='id').execute()
                    funcion.dirGoogle = file.get('id')
                    funcion.save()

                    # avance pal usuario
                    print("funcion, dir: {}".format(funcion.dirGoogle))

                    for indicador in funcion.indicador_set.all() :
                        file_metadata = {
                            'name' : '{}'.format(indicador.nombre),
                            'mimeType' : 'application/vnd.google-apps.folder',
                            'parents' : [funcion.dirGoogle]
                        }
                        file = service.files().create(body=file_metadata, fields='id').execute()
                        indicador.dirGoogle = file.get('id')
                        indicador.save()

                        # avance pal usuario
                        print("indicador, dir: {}".format(indicador.dirGoogle))
            else :
                print("WARN: El directorio de la accion {} ya existe!".format(dirAccion))

        # codigo para crear directorios de acciones POA
        # comentado por ahora por temas de seguridad
        '''
        for accion in Accion.objects.all() :
            file_metadata = {
                'name' : 'ACCION_{}'.format(accion.id_uaysen),
                'mimeType' : 'application/vnd.google-apps.folder',
                'parents' : [idDirBase]
            }
            file = service.files().create(body=file_metadata, fields='id').execute()
            accion.dirGoogle = file.get('id')
            accion.save()

            file_metadata = {
                'name' : '{}'.format('MDVs'),
                'mimeType' : 'application/vnd.google-apps.folder',
                'parents' : [accion.dirGoogle]
            }
            file = service.files().create(body=file_metadata, fields='id').execute()
            mdvDirId = file.get('id')
            for mdv in accion.mdv_set.all() :
                file_metadata = {
                    'name' : '{}'.format(mdv.nombre),
                    'mimeType' : 'application/vnd.google-apps.folder',
                    'parents' : [mdvDirId]
                }
                file = service.files().create(body=file_metadata, fields='id').execute()
                mdv.dirGoogle = file.get('id')
                mdv.save()

            file_metadata = {
                'name' : '{}'.format('Funciones'),
                'mimeType' : 'application/vnd.google-apps.folder',
                'parents' : [accion.dirGoogle]
            }
            file = service.files().create(body=file_metadata, fields='id').execute()
            funcionDirId = file.get('id')
            for funcion in accion.funcion_set.all() :
                file_metadata = {
                    'name' : '{}'.format(funcion.nombre),
                    'mimeType' : 'application/vnd.google-apps.folder',
                    'parents' : [funcionDirId]
                }
                file = service.files().create(body=file_metadata, fields='id').execute()
                funcion.dirGoogle = file.get('id')
                funcion.save()
                for indicador in funcion.indicador_set.all() :
                    file_metadata = {
                        'name' : '{}'.format(indicador.nombre),
                        'mimeType' : 'application/vnd.google-apps.folder',
                        'parents' : [funcion.dirGoogle]
                    }
                    file = service.files().create(body=file_metadata, fields='id').execute()
                    indicador.dirGoogle = file.get('id')
                    indicador.save()
        ''' 
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
