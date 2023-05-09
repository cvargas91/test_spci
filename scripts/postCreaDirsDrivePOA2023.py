'''
Crea la estructura de directorios en Google Drive

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
                'client_secret3.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pathToken, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('drive', 'v3', credentials=creds)
        
        #Cambiar idDirbase al id de la carpeta que contendrá el directorio de acciones POA 2023
        #idDirBase = '1Yd0TJM1cGFpXlObI9V4F8PbptjmaB110' 
        idDirBase = '1I_Mw4IF-f9NayM-UidOvLYW8TKXsW0G3' 

        cont = 0
        #for accion in Accion.objects.filter(origen="PMI") :
        for accion in Accion.objects.filter(anio=2023) :
            dirAccion = 'ACCION_{}'.format(accion.id_uaysen)
            query = "name='{}' and '{}' in parents".format(dirAccion, idDirBase)
            respuesta = service.files().list(q=query).execute()
            
            cont+=1

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

                # avance para el usuario
                print("accion: {}, dir: {}".format(accion.id_uaysen, accion.dirGoogle))

                file_metadata = {
                    #'name' : '{}'.format('MDVs'),
                    'name' : '{}'.format('Hitos'),
                    'mimeType' : 'application/vnd.google-apps.folder',
                    'parents' : [accion.dirGoogle]
                }
                file = service.files().create(body=file_metadata, fields='id').execute()
                hitoDirId = file.get('id')
                for hito in accion.hito_set.all() :
                    file_metadata = {
                        'name' : '{}'.format(hito.nombre),
                        'mimeType' : 'application/vnd.google-apps.folder',
                        'parents' : [hitoDirId]
                    }
                    file = service.files().create(body=file_metadata, fields='id').execute()
                    hito.dirGoogle = file.get('id')
                    hito.save()

                    # avance pal usuario
                    print("hito, dir: {}".format(hito.dirGoogle))

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
            hitoDirId = file.get('id')
            for mdv in accion.mdv_set.all() :
                file_metadata = {
                    'name' : '{}'.format(mdv.nombre),
                    'mimeType' : 'application/vnd.google-apps.folder',
                    'parents' : [hitoDirId]
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
