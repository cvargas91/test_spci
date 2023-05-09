'''
Carga actores que vienen de un PDF oficial de actores (catálogo)

Versiones (fecha;descripcion;autor)
04/01/2022; linea base; JGED
'''

import django
import csv
from webapp.models import *

ACTOR_CODIGO = 0
ACTOR_SIGLA = 1
ACTOR_NOMBRE = 2
ACTOR_DEPENDENCIA = 3

def hackSigla(sigla) :
    if sigla == 'EPYEC' :
        return 'EPYFC'
    if sigla in ['CONTRALOR (A)', 'CONTRALORA'] :
        return 'CU'
    if sigla == 'INV' :
        return 'DINV'
    return sigla
    
def run():
    if len(Actor.objects.all()) != 0 :
        print("Ya hay actores, no voy a cargar nada")
        return 0
    rutaActores = 'data_inicial/matriz_de_permisos_usuarios_SPCI_categorias.csv'
    with open(rutaActores, encoding='cp1252') as csvfile :
        pass
    django.setup()
    # se cargan todos los datos de los actores, salvo las categorias
    with open(rutaActores, encoding='cp1252') as csvfile :
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:

            dependencia = None
            categoria = row[0].strip()
            nombre = row[2].strip()
            sigla = row[3].strip().upper()
            cai = row[4].strip().upper()

            Actor.objects.create(
                nombre = nombre,
                id_uaysen = sigla,
                sigla = sigla,
                dependencia = dependencia,
                categoria = categoria,
                cai = cai
            )

    # TODO: usar funcion mas elegante para "rebobinar" el archivo
    # se cargan las dependencias
    with open(rutaActores, encoding='cp1252') as csvfile :
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            str_dependencia = row[1].strip().upper()
            sigla = row[3].strip().upper()
            if str_dependencia == "TODOS" :
                continue
            dependencia = Actor.objects.get(id_uaysen=str_dependencia.strip().upper())
            Actor.objects.filter(sigla = sigla).update(
                dependencia = dependencia
            )
            
