'''
elimina la bd
'''

import django
import csv
from webapp.models import *

NUM_FILAS_CADA_FUNCION = 5
NUM_FILAS_CADA_HITO = 3
PROCESO_ANIO = 2022

def run():
    if False :
        return
    django.setup()
    Accion.objects.all().delete()
    Rol.objects.all().delete()
    Plazo.objects.all().delete()
    Periodo.objects.all().delete()
    Estrategia.objects.all().delete()
    Actor.objects.all().delete()
    Funcion.objects.all().delete()
    Hito.objects.all().delete()
    MDV.objects.all().delete()
    Producto.objects.all().delete()
    Verificador.objects.all().delete()
    RetroEntrega.objects.all().delete()
    return