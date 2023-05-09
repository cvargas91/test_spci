'''
Carga acciones, roles y estrategias PMI previamente
pasadas a CSV

requisitos para funcionar
 - rezar ctm

Versiones (fecha;descripcion;autor)
29/11/2022; linea base; JGED
'''

import django
import csv
from webapp.models import *
from django.contrib.auth.models import User

PROCESO_ANIO = 2022
NUM_ITEMS_FUNCION = 4

DEPTOS_UAYSEN = ['DCNT', 'DCS', 'DCSH']

def hackSigla(sigla) :
    if sigla == 'EPYEC' :
        return 'EPYFC'
    if sigla in ['CONTRALOR (A)', 'CONTRALORA'] :
        return 'CU'
    if sigla == 'INV' :
        return 'DINV'
    return sigla

def run():
    # chequeo de archivos a cargar:
    # a)
    # - acciones PMI y sus responsables
    rutaAcciones = 'data_inicial/pmi/acciones.csv'
    with open(rutaAcciones, encoding='cp1252') as csvfile :
        pass
    # - roles (todos salvo responsables) de acciones PMI
    rutaRoles = 'data_inicial/pmi/roles.csv'
    with open(rutaRoles, encoding='cp1252') as csvfile :
        pass
    # - estrategias de las acciones PMI
    rutaEstrategias = 'data_inicial/pmi/estrategias.csv'
    with open(rutaEstrategias, encoding='cp1252') as csvfile :
        pass
    django.setup()
    
    # a)
    # carga de acciones PMI:
    with open(rutaAcciones, encoding='cp1252') as csvfile :
        lector = csv.reader(csvfile, delimiter=',', quotechar='"')
        numFila = 0
        posicionesMDVs = []
        posicionesHitos = []
        posicionesFunciones = []
        for fila in lector:
            # en la primera fila es posible contar los hitos
            # y los medios de verificación, pero no las funciones
            # ni cuantos indicadores tienen c/u, por eso, eso se
            # cuenta en la segunda (sí, una mierda)
            if numFila == 0 :
                for i in range(0, len(fila), 1) :
                    if 'hito' in fila[i].lower() :
                        posicionesHitos.append(i)
                    elif 'medio' in fila[i].lower() :
                        posicionesMDVs.append(i)
            elif numFila == 1 :
                for i in range(7, posicionesHitos[0], 1) :
                    if 'funci' in fila[i].strip().lower() :
                        posicionesFunciones.append(i)
                if len(posicionesFunciones) > 0 :
                    posicionesFunciones.append(posicionesFunciones[-1]+NUM_ITEMS_FUNCION+1)
            # se extraen los datos de la accion y se crea en BD
            # se aprovechan de crear los roles responsables,
            # funciones, hitos y medios de verificacion
            elif numFila >= 2 :
                # hack para que funcione la carga dinamica de indicadores
                actor = None
                sigla = hackSigla(fila[2].strip().upper())
                actor = Actor.objects.get(sigla=sigla)
                presupuesto = None
                if fila[6].strip() != '' :
                    presupuesto = ''.join(c for c in fila[6].strip() if c.isdigit())
                    presupuesto = int(presupuesto) if presupuesto else 0
                accion = Accion.objects.create(
                    id_uaysen = fila[1].strip(),
                    anio = PROCESO_ANIO,
                    titulo = fila[3].strip(),
                    objetivo = fila[4].strip(),
                    tipo = 'Misional' if fila[5].strip().lower() == 'misional' else 'Desarrollo',
                    presupuesto = presupuesto,
                    origen = "PMI"
                )
                Rol.objects.create(
                    accion = accion,
                    actor = actor,
                    tipo = 'Responsable'
                )
                for index, item in enumerate(posicionesFunciones[:-1]) :
                    if fila[item].strip() == '' :
                        continue
                    funcion = Funcion.objects.create(
                        accion = accion,
                        nombre = fila[item].strip(),
                    )
                    for subIndex in range(item+1, posicionesFunciones[index+1], NUM_ITEMS_FUNCION) :
                        if fila[subIndex].strip() == '' :
                            continue
                        Indicador.objects.create(
                            funcion = funcion,
                            nombre = fila[subIndex].strip(),
                            formula = fila[subIndex+1].strip(),
                            meta = fila[subIndex+2].strip().replace("%",""),
                            nombreVerificador = fila[subIndex+3].strip()
                        )             
                for index, item in enumerate(posicionesMDVs[:-1]) :
                    if fila[item].strip() == '' :
                        continue
                    mdv = MDV.objects.create(
                        accion = accion,
                        nombre = fila[item].strip()
                    )
                    for i in range(item+1, posicionesMDVs[index+1], 1) :
                        if fila[i].strip() == '' :
                            continue
                        CriterioMDV.objects.create(
                            criterio = fila[i].strip(),
                            mdv = mdv
                        )
                for item in posicionesHitos :
                    if fila[item].strip() == '' :
                        continue
                    str_plazo = fila[item+2].strip()
                    if len(str_plazo) > 0 :
                        mes = str_plazo.split('-')[0]
                        anio = str_plazo.split('-')[1]
                        obj_plazo = Plazo.objects.filter(plazo_mes=mes, plazo_anio=anio).first()
                        if not obj_plazo :
                            obj_plazo = Plazo.objects.create(plazo_anio=anio, plazo_mes=mes)
                        Hito.objects.create(
                            accion = accion,
                            nombre = fila[item].strip(),
                            descripcion = fila[item+1].strip(),
                            plazo = obj_plazo
                        )
            numFila+=1
    # b)
    # carga del resto de los roles (soporte, consultados e informados)
    with open(rutaRoles, encoding='cp1252') as csvfile :
        lector = csv.reader(csvfile, delimiter=',', quotechar='"')
        numFila = 0
        aprobador = -1
        soportes = []
        consultados = []
        informados = []
        for fila in lector:
            # se sacan los ids de las cabeceras
            if numFila == 0 :
                numColumna = 0
                for item in fila :
                    if 'aprobador' in item.strip().lower() :
                        aprobador = numColumna+1
                    if 'soporte' in item.strip().lower() :
                        soportes.append(numColumna+1)
                    if 'consultado' in item.strip().lower() :
                        consultados.append(numColumna+1)
                    if 'informado' in item.strip().lower() :
                        informados.append(numColumna+1)
                    numColumna+=1
            else :
                # se evitan casos con lineas en blanco que puedan botar el script
                if len(fila) <= 1 :
                    continue
                if len(fila) > 0 and (fila[0] == '' or fila[1] == ''):
                    continue
                id_uaysen = fila[0].strip().upper()
                accion = Accion.objects.filter(id_uaysen=id_uaysen).first()
                if not accion :
                    print("no encontré la accion {} (esto es MUY raro), en línea 198".format(id_uaysen))
                    continue
                escapes = ['', '#¡ref!', 'todos', 'tactico', 'dptos']
                for i in soportes :
                    if fila[i].strip().lower() not in escapes :
                        sigla = hackSigla(fila[i].strip().upper())
                        actor = Actor.objects.filter(sigla=sigla).first()
                        if not actor :
                            print("no encontre actor de sigla {} en la linea 186 o cerca de ahi".format(sigla))
                            continue
                        Rol.objects.create(
                            accion = accion,
                            actor = actor,
                            tipo = 'Soporte'
                        )
                for i in consultados :
                    if fila[i].strip().lower() not in escapes :
                        sigla = hackSigla(fila[i].strip().upper())
                        actor = Actor.objects.filter(sigla=sigla).first()
                        if not actor :
                            print("no encontré el actor {} en linea 198 o por ahí".format(sigla))
                            continue
                        Rol.objects.create(
                            accion = accion,
                            actor = actor,
                            tipo = 'Consultado'
                        )
                for i in informados :
                    if fila[i].strip().lower() not in escapes :
                        sigla = hackSigla(fila[i].strip().upper())
                        actor = Actor.objects.filter(sigla=sigla).first()
                        if not actor :
                            print("no encontré actor {} en línea 210".format(sigla))
                            continue
                        Rol.objects.create(
                            accion = accion,
                            actor = actor,
                            tipo = 'Informado'
                        )
            numFila+=1
    # c)
    # carga de estrategias
    with open(rutaEstrategias, encoding='cp1252') as csvfile :
        lector = csv.reader(csvfile, delimiter=',', quotechar='"')
        area=''
        if area in DEPTOS_UAYSEN :
            depto_estrategias_offset = 4
            next(lector)
            next(lector)
            filaOEs = next(lector)
            cantidadOEs = 0
            for item in filaOEs :
                if 'OE' in item :
                    cantidadOEs+=1
            next(lector)
            for fila in lector:
                for i in range(depto_estrategias_offset,cantidadOEs+depto_estrategias_offset,1) :
                    id_uaysen = 'PDE-{}-OE{}'.format(area[1:], i-depto_estrategias_offset+1)
                    estrategia = Estrategia.objects.get(id_uaysen=id_uaysen)
                    accion = Accion.objects.get(id_uaysen=fila[0].strip().upper())
                    if accion and estrategia not in accion.estrategias.all() :
                        accion.estrategias.add(estrategia)
        else :
            for fila in lector:
                accion = Accion.objects.filter(id_uaysen=fila[0].strip().upper()).first()
                if not accion :
                    print("no encontré accion '{}' (esto es MUY raro), en linea 267".format(fila[0].strip().upper()))
                    continue
                offset = 5
                for i in range(1+offset,20+offset) :
                    if fila[i].strip() != '' :
                        estrategia_str = 'PEDI-OE{}'.format(i-offset) if i-offset>=10 else 'PEDI-OE0{}'.format(i-offset)
                        estrategia = Estrategia.objects.get(id_uaysen=estrategia_str)
                        if estrategia not in accion.estrategias.all() :
                            accion.estrategias.add(estrategia)
                        
