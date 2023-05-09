'''
Carga las estrategias previamente pasadas a CSV

requisitos para funcionar
 - actores cargados (con sus siglas correctas)
 - proyectos cargados (con sus siglas correctas)
 - las acciones en csv con estructura correcta
'''

import django
import csv
from webapp.models import *

def run():
    if len(Estrategia.objects.all()) != 0 :
        print("Ya hay estrategias, no voy a cargar nada")
        return 0
    django.setup()
    with open('data_inicial/estrategias/Book1.csv', encoding='cp1252') as csvfile :
        lector = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(lector)
        for fila in lector:
            anioInicio = fila[3].strip().split('-')[0]
            anioFin = fila[3].strip().split('-')[1]
            if len(Periodo.objects.filter(anio_inicio=anioInicio, anio_fin=anioFin)) == 0 :
                Periodo.objects.create(
                    anio_inicio = anioInicio,
                    anio_fin = anioFin
                )
            estrategia = fila[0].strip().split('-')[0]
            tipoEstrategia = ''
            if 'PEDI' in estrategia :
                tipoEstrategia = 'PEDI'
            elif 'PDE' in estrategia :
                tipoEstrategia = 'PDE'
            elif 'PM' in estrategia :
                tipoEstrategia = 'PM'
            Estrategia.objects.create(
                id_uaysen = fila[0].strip(),
                tipo = tipoEstrategia,
                ambito = fila[1].strip(),
                descripcion = fila[2].strip(),
                periodo = Periodo.objects.get(anio_inicio=anioInicio, anio_fin=anioFin)
            )
