'''
Carga un temporal de la matriz Accion/Estrategia
'''

import django
import csv
from webapp.models import *

PROCESO_ANIO = 2022

def run():
    django.setup()
    series = []
    for a in Accion.objects.all().order_by('-id') :
        if a.id_uaysen.split('-')[0] != 'DPAC' :
            continue 
        data = []
        serieNombre = a.id_uaysen
        for e in Estrategia.objects.all() :
            if 'PEDI' not in e.id_uaysen :
                continue
            data.append({
                'x':e.id_uaysen,
                'y':1 if e in a.estrategias.all() else 0})
        series.append({
            'name':serieNombre,
            'data':data})
    if len(Meta.objects.all()) == 0 :
        Meta.objects.create(matrizAccionEstrategia = series)
    else :
        Meta.objects.all().update(matrizAccionEstrategia = series)
    return