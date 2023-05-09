'''
Carga acciones, roles, estrategias y dimensiones según POA2023 previamente
pasadas a CSV


Versiones (fecha;descripcion;autor)
29/11/2022; linea base; JGED
'''

import django
import csv
#from webapp.models import *
from webapp.models import *
from django.contrib.auth.models import User
from django.db.models import Count

PROCESO_ANIO = 2023
#Validar uso de esta variable
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

# def hackEliminaRepetidosROLES(accion, actor, rol):
#     print ("===============================================")
#     print("ELIMINA REPETIDO para accion=",accion.id_uaysen, ", Actor=", actor.sigla, " y ROL = ", rol)
#     duplicados=Rol.objects.filter(accion=accion, actor=actor, tipo=rol)

#     print("ROLES DUPLICADOS TOTAL = ", duplicados.count())

#     for rol in duplicados:
#         print(rol)
#     print ("===============================================")

# def validaAccionesDuplicadas(acciones):
#     print ("===============================================")
#     print("ACCIONES DUPLICADOS TOTAL = ", acciones.count())
#     for accion in acciones:
#         print("DUPLICIDADES ", accion)
#     print ("===============================================")


def run():
    print("INICIO DE SCRIPT CARGA_DATOS_2023")
    # chequeo de archivos a cargar:
    # a)
    # - acciones PMI y sus responsables
    rutaAcciones = 'data_inicial/poa2023/acciones2023.csv'
    with open(rutaAcciones, encoding='cp1252') as csvfile :
        pass
    # - roles (todos salvo responsables) de acciones PMI
    rutaRoles = 'data_inicial/poa2023/roles2023.csv'
    with open(rutaRoles, encoding='cp1252') as csvfile :
        pass
    # - estrategias de las acciones PMI
    rutaEstrategias = 'data_inicial/poa2023/estrategias2023.csv'
    with open(rutaEstrategias, encoding='cp1252') as csvfile :
        pass
    # - estrategias de las acciones PMI
    rutaDimensiones = 'data_inicial/poa2023/dimensiones2023.csv'
    with open(rutaDimensiones, encoding='cp1252') as csvfile :
        pass
    django.setup()
    # a)
    # carga de acciones PMI:
    with open(rutaAcciones, encoding='cp1252') as csvfile :
        lector = csv.reader(csvfile, delimiter=';', quotechar='"')
        numFila = 0
        # Se mantiene el uso de MDVs ya que sólo implica una relación vacía.
        posicionesMDVs = []
        posicionesHitos = []
        posicionesFunciones = []
        encabezado = next(lector)  # saltar la primera fila
        for fila in lector:
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
            
            elif numFila >= 2 :
                # hack para que funcione la carga dinamica de indicadores
                actor = None
                sigla = hackSigla(fila[2].strip().upper())
                #actor = Actor.objects.get(sigla=sigla)

                try:
                        actor = Actor.objects.get(sigla=sigla)
                except Actor.DoesNotExist:
                        print("Actor No existe en BD = '", sigla, "'")
                        print("Acción Asociada       = ", fila[1].strip())
                        #dimension = Dimension.objects.create(nombre=fila[i].strip(), texto_ley="")

                presupuesto = None
                if fila[6].strip() != '' :
                    presupuesto = ''.join(c for c in fila[6].strip() if c.isdigit())
                    presupuesto = int(presupuesto) if presupuesto else 0
                acciones = Accion.objects.filter(id_uaysen=fila[1].strip())
                if acciones.exists():
                    accion = acciones[0]
                else:
                    accion = None
                if not accion:
                    accion = Accion.objects.create(
                        id_uaysen = fila[1].strip(),
                        anio = PROCESO_ANIO,
                        titulo = fila[3].strip(),
                        objetivo = fila[4].strip(),
                        # tipo = 'Misional' if fila[5].strip().lower() == 'misional' else 'Desarrollo',
                        tipo = '',
                        presupuesto = presupuesto,
                        origen = "PMI" if 'PMI' in fila[1].strip() else "URY" if 'URY' in fila[1].strip() else "TRANSVERSAL" if 'TRANSVERSAL' in fila[1].strip() else ""
                    )
                else:
                    accion.id_uaysen = fila[1].strip()
                    accion.anio = PROCESO_ANIO
                    accion.titulo = fila[3].strip()
                    accion.objetivo = fila[4].strip()
                    accion.tipo = ''
                    accion.presupuesto = presupuesto
                    accion.origen = "PMI" if 'PMI' in fila[1].strip() else "URY" if 'URY' in fila[1].strip() else "TRANSVERSAL" if 'TRANSVERSAL' in fila[1].strip() else ""
                    accion.save()
                    #validaAccionesDuplicadas(acciones)
                
                #hackEliminaRepetidosROLES(accion,actor,'Responsable')
                if actor:
                    roles = Rol.objects.filter(accion = accion.id, actor = actor.id, tipo = "Responsable")
                    if roles.exists():
                        rol = roles[0]
                    else:
                        rol = None

                    if not rol:    
                        Rol.objects.create(
                            accion = accion,
                            actor = actor,
                            tipo = 'Responsable'
                        )
                    else:
                        rol.accion = accion
                        rol.actor = actor
                        rol.tipo = 'Responsable'
                        rol.save()
                else:
                    print("NO SE CREA O ACTUALIZA ROL RESPONSABLE - Actor ", sigla, " NO EXISTE EN BD")
                    print("ACCION = ", fila[1].strip())
                    print("=============================")

                for index, item in enumerate(posicionesFunciones[:-1]) :
                    if fila[item].strip() == '' :
                        continue
                    
                    funciones = Funcion.objects.filter(accion=accion.id, nombre=fila[item].strip())
                    
                    if funciones.exists():
                        funcion = funciones[0]
                    else:
                        funcion = None

                    if not funcion:
                        funcion = Funcion.objects.create(accion=accion, nombre=fila[item].strip())
                    else:
                        funcion.accion = accion
                        funcion.nombre = fila[item].strip()
                        funcion.save()                    

                    for subIndex in range(item+1, posicionesFunciones[index+1], NUM_ITEMS_FUNCION) :
                        nombreIndicador = fila[subIndex].strip()
                        if nombreIndicador == '' :
                            nombreIndicador = fila[subIndex+1].strip()
                        if nombreIndicador == '' :
                            continue
                        indicadores = Indicador.objects.filter(funcion = funcion.id,
                            nombre = nombreIndicador,
                            formula = fila[subIndex+1].strip(),
                            nombreVerificador = fila[subIndex+3].strip())
                        
                        if indicadores.exists():
                            indicador = indicadores[0]
                        else:
                            indicador = None

                        tipo_meta = 0

                        if "%" in fila[subIndex+2].strip():                            
                            tipo_meta = 2
                        else:
                            tipo_meta = 1  
                            
                        if not indicador:
                            indicador = Indicador.objects.create(
                                funcion = funcion,
                                nombre = nombreIndicador,
                                formula = fila[subIndex+1].strip(),
                                meta = fila[subIndex+2].strip().replace("%",""),
                                tipo_indicador = tipo_meta,
                                nombreVerificador = fila[subIndex+3].strip()
                            )
                        else:
                            indicador.funcion = funcion
                            indicador.nombre  = nombreIndicador
                            indicador.formula = fila[subIndex+1].strip()
                            indicador.meta = fila[subIndex+2].strip().replace("%","")
                            indicador.tipo_indicador = tipo_meta
                            indicador.nombreVerificador = fila[subIndex+3].strip()
                            indicador.save()
                    
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

                        hitos = Hito.objects.filter(
                                accion = accion.id,
                                nombre = fila[item].strip(),
                                descripcion = fila[item+1].strip()
                            )

                        if hitos.exists():
                            hito = hitos[0]
                        else:
                            hito = None
                            
                        if not hito:
                            hito=Hito.objects.create(
                                    accion = accion,
                                    nombre = fila[item].strip(),
                                    descripcion = fila[item+1].strip(),
                                    plazo = obj_plazo
                            )
                        else:
                            hito.accion = accion
                            hito.nombre = fila[item].strip()
                            hito.descripcion = fila[item+1].strip()
                            hito.plazo = obj_plazo
                            hito.save()
                    else:
                        #CONTROL HITOS SIN PLAZO
                        hitos = Hito.objects.filter(
                                accion = accion.id,
                                nombre = fila[item].strip(),
                                descripcion = fila[item+1].strip()
                            )
                        
                        if hitos.exists():
                            hito = hitos[0]
                        else:
                            hito = None
                            
                        if not hito:
                            hito=Hito.objects.create(
                                    accion = accion,
                                    nombre = fila[item].strip(),
                                    descripcion = fila[item+1].strip(),
                            )
                        else:
                            hito.accion = accion
                            hito.nombre = fila[item].strip()
                            hito.descripcion = fila[item+1].strip()
                            hito.save()
                            
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
        encabezado = next(lector)  # saltar la primera fila
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
                        else:
                        #hackEliminaRepetidosROLES(accion,actor,'Soporte')

                            roles = Rol.objects.filter(accion = accion.id, actor = actor.id, tipo = "Soporte")
                            if roles.exists():
                                rol = roles[0]
                            else:
                                rol = None

                            if not rol:
                                Rol.objects.create(
                                    accion = accion,
                                    actor = actor,
                                    tipo = 'Soporte'
                                )
                            else:
                                rol.accion = accion.id
                                rol.actor = actor.id
                                rol.tipo = 'Soporte'
                                rol.save()
                                
                        #     Rol.objects.create(
                        #     accion = accion,
                        #     actor = actor,
                        #     tipo = 'Soporte'
                        # )
                        
                for i in consultados :
                    if fila[i].strip().lower() not in escapes :
                        sigla = hackSigla(fila[i].strip().upper())
                        actor = Actor.objects.filter(sigla=sigla).first()
                        if not actor :
                            print("no encontré el actor {} en linea 198 o por ahí".format(sigla))
                            continue
                       # hackEliminaRepetidosROLES(accion,actor,'Consultado')
                        else:
                            roles = Rol.objects.filter(accion = accion.id, actor = actor.id, tipo = "Consultado")
                            if roles.exists():
                                rol = roles[0]
                            else:
                                rol = None

                            if not rol:
                                Rol.objects.create(
                                    accion = accion,
                                    actor = actor,
                                    tipo = 'Consultado'
                                )
                            else:
                                rol.accion = accion.id
                                rol.actor = actor.id
                                rol.tipo = 'Consultado'
                                rol.save()
                        # Rol.objects.create(
                        #     accion = accion,
                        #     actor = actor,
                        #     tipo = 'Consultado'
                        #    )
                        
                for i in informados :
                    if fila[i].strip().lower() not in escapes :
                        sigla = hackSigla(fila[i].strip().upper())
                        actor = Actor.objects.filter(sigla=sigla).first()
                        if not actor :
                            print("no encontré actor {} en línea 210".format(sigla))
                            continue
                        #hackEliminaRepetidosROLES(accion,actor,'Informado')
                        else:
                            roles = Rol.objects.filter(accion = accion.id, actor = actor.id, tipo = "Informado")
                            if roles.exists():
                                rol = roles[0]
                            else:
                                rol = None

                            if not rol:
                                Rol.objects.create(
                                    accion = accion,
                                    actor = actor,
                                    tipo = 'Informado'
                                )
                            else:
                                rol.accion = accion.id
                                rol.actor = actor.id
                                rol.tipo = 'Informado'
                                rol.save()

                        # Rol.objects.create(
                        #     accion = accion,
                        #     actor = actor,
                        #     tipo = 'Informado'
                        # )
                        
            numFila+=1
    # c)
    
    # carga de estrategias
    with open(rutaEstrategias, encoding='cp1252') as csvfile :
        lector = csv.reader(csvfile, delimiter=';', quotechar='"')
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
            next(lector)
            next(lector)
            next(lector)
            next(lector)
            for fila in lector:
                #accion = Accion.objects.get(id_uaysen=fila[1].strip().upper())
                accion = Accion.objects.filter(id_uaysen=fila[1].strip().upper()).last()

                if not accion:
                    print("ACCION ", fila[1].strip().upper(), " no ha sido ingresada")
                    print ("ACCION EN ESTRATEGIAS => ", accion)
                else:
                    for i in range(6,25):                    
                        if fila[i].strip() != '' :
                            estrategia_str = 'PEDI-OE{}'.format(i-5) if i-5>=10 else 'PEDI-OE0{}'.format(i-5)
                            estrategia = Estrategia.objects.get(id_uaysen=estrategia_str)
                            if estrategia not in accion.estrategias.all() :
                                accion.estrategias.add(estrategia)
                # for i in range(25,40) :
                #     if fila[i].strip() != '' :
                #         estrategia_str = 'PM{}'.format(i-25)
                #         estrategia = Estrategia.objects.get(id_uaysen=estrategia_str)
                        
                #         if estrategia not in accion.estrategias.all() :
                #             accion.estrategias.add(estrategia)

# b)
    # carga del resto de los roles (soporte, consultados e informados)
    with open(rutaDimensiones, encoding='cp1252') as csvfile :
        lector = csv.reader(csvfile, delimiter=';', quotechar='"')
        numFila = 0
        next(lector)  # saltar la primera fila
        next(lector)
        for fila in lector:
            accion = Accion.objects.filter(id_uaysen=fila[0].strip().upper()).last()
            
            #next(fila)
            for i in range(1, len(fila)):
                if(len(fila[i]) > 0):
                    try:
                        dimension = Dimension.objects.get(nombre=fila[i].strip())
                    except Dimension.DoesNotExist:
                        dimension = Dimension.objects.create(nombre=fila[i].strip(), texto_ley="")
                    
                    if dimension not in accion.dimensiones.all():
                            accion.dimensiones.add(dimension)
                    # dimension = Dimension.objects.filter(nombre=fila[i].strip())
                    # if dimension.exists():
                    #     accion.dimensiones.add(dimension.first())
                    # else:                        
                    #     dimension = Dimension.objects.create(nombre=fila[i].strip(), texto_ley="")
                    #     accion.dimensiones.add(dimension)
        print ("FIN SCRIPT CARGA_DATOS_2023")
