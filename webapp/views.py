import mimetypes
from django.views.generic import ListView, View
import sys
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from spci.settings import STATIC_ROOT, STATIC_URL
from .models import Accion, Actor, PerfilUsuario, Meta, Estrategia, \
    nombresRol as opcionesRoles, \
    tiposAccion as opcionesTipos, \
    tiposTactica as opcionesTacticas, \
    meses as opcionesMeses, \
    Plazo
## Para reportes ##
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
##
from .serializers import *
from django.db.models import Q, Sum,FloatField
from django.db.models.functions import Cast
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, authentication_classes
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import os

# def. de constantes
CALLBACK_URI = '/gCallback'
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"]
SUBDOMAIN_URL = os.getenv('API_GOOGLE_SUBDOMAIN_URL')
LOCAL = eval(os.getenv('API_GOOGLE_LOCAL'))
# fin def. de constantes

def getPerfilUsuario(request) :    
    perfilUsuario = request.user.perfilusuario_set.first()
    if 'perfil' in request.session and request.session['perfil'] != perfilUsuario.actor.nombre :        
        return request.user.perfilusuario_set.get(actor__nombre=request.session['perfil'])
    return perfilUsuario
        
def index(request):
    if request.user and request.user.is_authenticated :
        perfiles = User.objects.filter(email=request.user.email).first().perfilusuario_set.all()
        cantidadPerfiles = len(perfiles)
        if cantidadPerfiles == 0 :
            return render(request, 'webapp/sinPerfil.html', {})
        elif cantidadPerfiles > 1 :
            detallePerfiles = []
            for perfil in perfiles :
                detallePerfiles.append(
                    {'perfil' : perfil.actor.nombre,
                    'es_encargado' : perfil.es_encargado})
            return render(request, 'webapp/escogePerfil.html',
                {'nombreUsuario' : '{} {}'.format(request.user.first_name, request.user.last_name),
                'perfiles' : detallePerfiles})
        return redirect('/app')
    else :
        return redirect('/gRedirect')

@require_http_methods(["POST"])
def seteaPerfil(request):
    request.session['perfil'] = request.POST['perfil']
    return redirect('/app')

def datosIniciales(request) :
    perfilUsuario = getPerfilUsuario(request)
    return JsonResponse({
        'usuario': {
            'id' : request.user.id,
            'username' : request.user.username,
            'nombre' : request.user.first_name,
            'apellido' : request.user.last_name,
            'perfil' : {
                'actor_id' : perfilUsuario.actor.id,
                'actor_nombre' : perfilUsuario.actor.nombre,
                'area_sigla' : perfilUsuario.actor.dependencia.sigla if perfilUsuario.actor.dependencia else perfilUsuario.actor.sigla,
                'esEncargado' : perfilUsuario.es_encargado,
                'esAnalistaUPCI' : perfilUsuario.es_analistaUPCI,
                'esMultiPerfil' : len(request.user.perfilusuario_set.all()) > 1,
                'foto' : perfilUsuario.foto,
            }
        },
        'opciones' : {
            'actores' : list(map(lambda x: {'value':x[0], 'label':x[1]}, list(Actor.objects.values_list('id', 'nombre')))),
            'roles' : ["Todos"] + list(map(lambda x : x[0], opcionesRoles)),
            'tipos' : ["Todos"] + list(map(lambda x : x[0], opcionesTipos)),
            'tacticas' : ["Todas"] + list(map(lambda x : x[0], opcionesTacticas)),
            'meses' : ["Todos"] + list(map(lambda x : x[0], opcionesMeses))
        }
    })
    
def gRedirect(request) :
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=SCOPES)
    flow.redirect_uri = "https://{}{}".format(SUBDOMAIN_URL, CALLBACK_URI)
    authorization_url, state = flow.authorization_url(access_type='offline')
    return redirect(authorization_url)

def gCallback(request) :
    state = request.GET['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        state=state)

    authorization_response = None
    flow.redirect_uri = "https://{}{}".format(SUBDOMAIN_URL, CALLBACK_URI)
    uri_https = str(request.build_absolute_uri()).replace("http://", "https://")
    #authorization_response = request.build_absolute_uri()
    authorization_response = uri_https
    try :
        flow.fetch_token(authorization_response=authorization_response)
    except :
        return render(request, 'webapp/error.html', {'error' : str(sys.exc_info())})
    credentials = flow.credentials
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    if user_info['verified_email'] and user_info['hd'] =='uaysen.cl' :
        current_user = User.objects.filter(username=user_info['email']).first()
        if not current_user :
            return render(request, 'webapp/sinUsuario.html', {})
        for perfil in current_user.perfilusuario_set.all() :
            perfil.sesion = {
                'token' : credentials.token,
                'refresh_token' : credentials.refresh_token,
                'token_uri' : credentials.token_uri,
                'client_id' : credentials.client_id,
                'client_secret' : credentials.client_secret,
                'scopes' : credentials.scopes
            }
            perfil.save()
        login(request, current_user)
    else :
        raise PermissionDenied()
    return redirect('/')

def getCredentials(request) :
    perfilUsuario = getPerfilUsuario(request)    
    return JsonResponse({'g_access_token': perfilUsuario.sesion["token"]})

def app(request):
    context = {'state': 'ok'}
    return render(request, 'webapp/app.html', context)

class HitoViewSet(viewsets.ModelViewSet):
    queryset = Hito.objects.all()
    serializer_class = HitoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['accion']

class FuncionViewSet(viewsets.ModelViewSet):
    queryset = Funcion.objects.all()
    serializer_class = FuncionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['accion']

class IndicadorViewSet(viewsets.ModelViewSet):
    queryset = Indicador.objects.all()
    serializer_class = IndicadorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['funcion']

    @action(detail=False, methods=['get'])
    def metaPorFuncion(self, request):
        id_funcion = request.query_params['funcion']
        total_metas = Indicador.objects.filter(funcion=id_funcion).annotate(as_float=Cast('meta', FloatField())).aggregate(valor=Sum('as_float'))
        return JsonResponse({"datos" : 
            {
                "total_meta_funcion" : total_metas
            }})

class MDVViewSet(viewsets.ModelViewSet):
    queryset = MDV.objects.all()
    serializer_class = MDVSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['accion']

    @action(detail=False, methods=['get'])
    def mdvsProductosReporte (self, request):
        id_accion = request.query_params['accion']
        mdvs = MDV.objects.filter(accion__hito=id_accion, estado="Finalizado")
        
        verificadorSerializados = self.get_serializer(mdvs, many=True)
        return JsonResponse({"datos" : 
        {"reporte-hito" : verificadorSerializados.data,
            
        }})


class AccionViewSet(viewsets.ModelViewSet):
    queryset = Accion.objects.all()
    serializer_class = AccionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['objetivo', 'tipo', 'anio']

    @action(detail=False, methods=['get'])
    def estrategias(self, request):
        return JsonResponse({'series': Meta.objects.all().first().matrizAccionEstrategia})
    
    @action(detail=False, methods=['get'], url_path=r'anios_unicos/(?P<accion>[^/.]+)')
    def anios_unicos(self, request,accion, *args, **kwargs):
        anios = Accion.objects.order_by('anio').values_list('anio', flat=True).distinct()
        return JsonResponse({'periodo': list(anios)})
    
    @action(detail=False, methods=['get'], url_path=r'origen_unicos/(?P<accion>[^/.]+)')
    def origen_unicos(self, request,accion, *args, **kwargs):
        # origenes = Accion.objects.order_by('origen').values_list('origen', flat=True).distinct()
        # return JsonResponse({'origenes': list(origenes)})
        acciones = Accion.objects.order_by('origen').values_list('origen', 'proyecto','anio', 'id_uaysen')
        origenes = []
        for accion in acciones:
            if(accion[2] == 2022):
                if(accion[1]!= None):
                    origenes.append('URY')
                else:
                    origenes.append('TRANSVERSAL')
            else:
                origenes.append(accion[0])

        return JsonResponse({'origenes': list(set(origenes))})  

    @action(detail=False, methods=['get'], url_path=r'hitosyfunciones/(?P<accion>[^/.]+)')
    def hitosyfunciones(self, request, accion, *args, **kwargs) :
        funciones = list(map(lambda x: {'value':x[0], 'label':x[1]}, list(Funcion.objects.filter(accion__id=accion).values_list('id', 'nombre'))))
        hitos = list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion__id=accion).values_list('id', 'nombre', 'descripcion', 'plazo'))))
        
        for hito in hitos:
            plazo = list(map(lambda x: {'anio':x[0], 'mes':x[1]}, list(Plazo.objects.filter(id=hito['plazo']).values_list('plazo_anio','plazo_mes'))))
            hito['plazo'] = plazo
        
        #return JsonResponse({ 'funciones' : list(map(lambda x: {'value':x[0], 'label':x[1]}, list(Funcion.objects.filter(accion__id=accion).values_list('id', 'nombre')))) , 'hitos' : list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion__id=accion).values_list('id', 'nombre', 'descripcion', 'plazo')))) })
        return JsonResponse({
            'funciones' : funciones,
            'hitos' : hitos
        })
    
    @action(detail=False, methods=['get'], url_path=r'mdvsFuncionesEhitos/(?P<accion>[^/.]+)')
    def mdvsFuncionesEhitos(self, request, accion, *args, **kwargs) :
        mdvs = list(map(lambda x: {'value':x[0], 'label':x[1]}, list(MDV.objects.filter(accion__id=accion).values_list('id','nombre'))))
        hitos = list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion__id=accion).values_list('id', 'nombre', 'descripcion', 'plazo'))))

        for hito in hitos:
            plazo = list(map(lambda x: {'anio':x[0], 'mes':x[1]}, list(Plazo.objects.filter(id=hito['plazo']).values_list('plazo_anio','plazo_mes'))))
            hito['plazo'] = plazo

        return JsonResponse({
            'mdvs' : mdvs,
            'hitos' : hitos
        })
        #return JsonResponse({'hitos' : list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion__id=accion).values_list('id', 'nombre', 'descripcion', 'plazo')))) ,'mdvs' : list(map(lambda x: {'value':x[0], 'label':x[1]}, list(MDV.objects.filter(accion__id=accion).values_list('id','nombre'))))})

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all().order_by('-nombre')
    serializer_class = ActorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    @action(detail=False, methods=['get'])
    def getActores(self, request):  
        actores = Actor.objects.all().order_by('nombre')
        actoresSerializados = self.get_serializer(actores, many=True)
        return JsonResponse({'datos': actoresSerializados.data})

    def getActoresPanel (self, request):
        actores = Actor.objects.filter(id__in=request)
        actoresSerializados = self.get_serializer(actores, many=True)
        return JsonResponse({"datos" : 
            {
                "detalleActores" : actoresSerializados.data,
            }
        })
    
    @action(detail=False, methods=['get'])
    def getDependencias(self, request):  
        actores = Actor.objects.filter(dependencia__dependencia__isnull=True).exclude(categoria='todos').order_by('-nombre')
        #actores = Actor.objects.filter(dependencia__isnull=True).order_by('-nombre')
        actoresSerializados = self.get_serializer(actores, many=True)
        return JsonResponse({'datos': ["Todos"] + actoresSerializados.data})
    
    @action(detail=False, methods=['get'])
    def getDireccion(self, request):
        dependencia = request.query_params['dependencia']
        actores = Actor.objects.filter(dependencia=dependencia).order_by('-nombre').exclude(es_direccion=True)
        actoresSerializados = self.get_serializer(actores, many=True)
        return JsonResponse({'datos': ["Todos"] + actoresSerializados.data})

    @action(detail=False, methods=['get'])
    def getDirecciones(self, request):
        actores = Actor.objects.filter(es_direccion=True)
        actoresSerializados = self.get_serializer(actores, many=True)
        
        return JsonResponse({'datos': ["Todos"] + actoresSerializados.data})
    
    @action(detail=False, methods=['get'])
    def getUnidades(self, request):
        actores = Actor.objects.filter(es_direccion=False)
        actoresSerializados = self.get_serializer(actores, many=True)
        
        return JsonResponse({'datos': ["Todos"] + actoresSerializados.data})

class VerificadorViewSet(viewsets.ModelViewSet):
    queryset = Verificador.objects.all().order_by('-id')
    serializer_class = VerificadorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario']

class VerificadorDepthViewSet(viewsets.ModelViewSet):
    queryset = Verificador.objects.all().order_by('-id')
    serializer_class = VerificadorDepthSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'estado', 'indicador','valor']

    def getVerificadoresUnidad(self, sinMi, request) :
        perfilUsuario = getPerfilUsuario(request)
        verificadores = Verificador.objects.distinct().exclude(usuario=request.user).\
            filter(indicador__funcion__accion__rol__actor=perfilUsuario.actor) \
            if sinMi else \
            Verificador.objects.distinct().filter(indicador__funcion__accion__rol__actor=perfilUsuario.actor, usuario=request.user)
        verificadores_borrador = verificadores.filter(estado="Borrador")
        verificadores_enviado_Lider = verificadores.filter(estado="Enviado al líder")
        verificadores_enviado_UPCI = verificadores.filter(estado="Enviado a UPCI")
        verificadores_finalizado = verificadores.filter(estado="Finalizado")
        verificadores_rechazado_lider = verificadores.filter(estado="Rechazado por líder")
        verificadores_rechazado_UPCI = verificadores.filter(estado="Rechazado por UPCI")
        serializer_borrador = self.get_serializer(verificadores_borrador, many=True)
        serializer_enviado_Lider = self.get_serializer(verificadores_enviado_Lider, many=True)
        serializer_enviado_UPCI = self.get_serializer(verificadores_enviado_UPCI, many=True)
        serializer_finalizado = self.get_serializer(verificadores_finalizado, many=True)
        serializer_rechazo_lider = self.get_serializer(verificadores_rechazado_lider, many=True)
        serializer_rechazo_UPCI = self.get_serializer(verificadores_rechazado_UPCI, many=True)
        return {"datos" : {"borradores" : serializer_borrador.data,
                            "enviados_Lider" : serializer_enviado_Lider.data,
                            "enviados_UPCI" : serializer_enviado_UPCI.data,
                            "rechazados_Lider" : serializer_rechazo_lider.data,
                            "rechazados_UPCI" : serializer_rechazo_UPCI.data,
                            "finalizados" : serializer_finalizado.data}}
    
    @action(detail=False, methods=['get'])
    def verificadoresUnidadSinMi(self, request):
        return JsonResponse(self.getVerificadoresUnidad(True, request))

    @action(detail=False, methods=['get'])
    def misVerificadores(self, request):
        return JsonResponse(self.getVerificadoresUnidad(False, request))

    @action(detail=False, methods=['get'])
    def verificadorPorIndicador(self, request):
        id_indicador = request.query_params['indicador']
        verificadoresPorIndicador = Verificador.objects.filter(indicador=id_indicador, estado="Finalizado")
        total_avances= Verificador.objects.filter(indicador=id_indicador, estado="Finalizado").annotate(as_float=Cast('valor', FloatField())).aggregate(valor=Sum('as_float'))
        verificadorSerializados = self.get_serializer(verificadoresPorIndicador, many=True)
        return JsonResponse({"datos" : 
            {"verificadores" : verificadorSerializados.data,
            "total_avances" : total_avances
            }})

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('-id')
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'mdv', 'estado']

class ProductoDepthViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('-id')
    serializer_class = ProductoDepthSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'mdv', 'estado']

    def getProductosUnidad(self, sinMi, request) :
        perfilUsuario = getPerfilUsuario(request)
        #filter(mdv__accion__rol__actor=perfilUsuario.actor) \
        productos = Producto.objects.distinct().exclude(usuario=request.user).\
            filter(Q(mdv__isnull = False, mdv__accion__rol__actor=perfilUsuario.actor) | \
            Q(mdv__isnull = True, hitos__accion__rol__actor=perfilUsuario.actor)) \
            if sinMi else \
            Producto.objects.distinct().filter(Q(mdv__isnull = False, mdv__accion__rol__actor=perfilUsuario.actor) | Q(mdv__isnull = True, hitos__accion__rol__actor=perfilUsuario.actor), usuario=request.user)
            #Producto.objects.distinct().filter(mdv__accion__rol__actor=perfilUsuario.actor, usuario=request.user)
        
        productos_borrador = productos.filter(estado="Borrador")
        productos_enviado_Lider = productos.filter(estado="Enviado al líder")
        productos_enviado_UPCI = productos.filter(estado="Enviado a UPCI")
        productos_rechazado_lider = productos.filter(estado="Rechazado por líder")
        productos_rechazado_UPCI = productos.filter(estado="Rechazado por UPCI")
        productos_finalizado = productos.filter(estado="Finalizado")
        serializer_borrador = self.get_serializer(productos_borrador, many=True)
        serializer_enviado_Lider = self.get_serializer(productos_enviado_Lider, many=True)
        serializer_enviado_UPCI = self.get_serializer(productos_enviado_UPCI, many=True)
        serializer_rechazo_lider = self.get_serializer(productos_rechazado_lider, many=True)
        serializer_rechazo_UPCI = self.get_serializer(productos_rechazado_UPCI, many=True)
        serializer_finalizado = self.get_serializer(productos_finalizado, many=True)
        return {"datos" : {"borradores" : serializer_borrador.data,
                            "enviados_Lider" : serializer_enviado_Lider.data,
                            "enviados_UPCI" : serializer_enviado_UPCI.data,
                            "rechazados_Lider" : serializer_rechazo_lider.data,
                            "rechazados_UPCI" : serializer_rechazo_UPCI.data,
                            "finalizados" : serializer_finalizado.data}}

    def getTodosProductosUnidad(self, request) :
        productos = Producto.objects.filter(actor=request.actor)
        productos_unidad_serializados = self.get_serializer(productos, many=True)
        return JsonResponse({"datos" : 
            {"productos" : productos_unidad_serializados.data }})
    
    @action(detail=False, methods=['get'])
    def productosUnidadSinMi(self, request):
        return JsonResponse(self.getProductosUnidad(True, request))

    @action(detail=False, methods=['get'])
    def misProductos(self, request):
        return JsonResponse(self.getProductosUnidad(False, request))

    @action(detail=False, methods=['get'])
    def productosUnidad(self, request):
        return JsonResponse(self.getTodosProductosUnidad(False, request))

    @action(detail=False, methods=['get'])
    def hitosReporte (self, request):
        id_accion = request.query_params['accion']
        return JsonResponse({
            'mdv' : list(map(lambda x: {'value':x[0], 'hitos':x[1]}, list(Producto.objects.filter(mdv__accion=id_accion,estado="Finalizado").values_list('mdv','hitos'))))
            })

class RetroEntregaViewSet(viewsets.ModelViewSet):
    queryset = RetroEntrega.objects.all().order_by('-modificado')
    serializer_class = RetroEntregaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'producto', 'verificador']

    @action(detail=False, methods=['get'])
    def misRetroalimentaciones(self, request):
        misRetrosProductos = RetroEntrega.objects.filter(producto__usuario=request.user)    
        misRetrosVerificadores = RetroEntrega.objects.filter(verificador__usuario=request.user)
        retroProductosSerializados = self.get_serializer(misRetrosProductos, many=True)
        retroVerificadoresSerializados = self.get_serializer(misRetrosVerificadores, many=True)
        
        for retroVerificador, retroVerificadorSerializado in zip(misRetrosVerificadores,retroVerificadoresSerializados.data):
            retroVerificadorSerializado['accion'] = retroVerificador.verificador.indicador.funcion.accion.id_uaysen

        for retroProducto, retroProductoSerializado in zip(misRetrosProductos, retroProductosSerializados.data):
            retroProductoSerializado['accion'] = retroProducto.producto.mdv.accion.id_uaysen if (retroProducto.producto.mdv and retroProducto.producto.mdv.accion) else retroProducto.producto.hitos.first().accion.id_uaysen
            #retroProductoSerializado['accion'] = retroProducto.producto.mdv.accion.id_uaysen

        return JsonResponse({'datos' : 
            {
            'productos' :  retroProductosSerializados.data,
            'verificadores' :  retroVerificadoresSerializados.data
            }
        })

class ReportesViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor','id']
    http_method_names = ['patch','post','get']

    @action(detail=False, methods=['get','post'])
    def misReportes (self, request):
        misReportes = Reporte.objects.filter(estado="Borrador", usuario=request.user, tipo="POA")
        misReportesPMI = Reporte.objects.filter(estado="Borrador", usuario=request.user, tipo="PMI")
        
        reportesSerializados = self.get_serializer(misReportes, many=True)
        reportesSerializadosPMI = self.get_serializer(misReportesPMI, many=True)
        return JsonResponse({'datos' : 
            {
            'borradores' :  reportesSerializados.data,
            'borradoresPMI' :  reportesSerializadosPMI.data,
            }
        })

    @action(detail=False, methods=['get'])
    def reportesUpci (self, request):
        reportesUpci = Reporte.objects.filter(estado="Finalizado", tipo="POA")
        reportesUpciPMI = Reporte.objects.filter(estado="Finalizado", tipo="PMI")
        reportesSerializados = self.get_serializer(reportesUpci, many=True)
        reportesSerializadosPMI = self.get_serializer(reportesUpciPMI, many=True)
        return JsonResponse({'datos' : 
            {
            'finalizados' :  reportesSerializados.data,
            'finalizadosPMI' :  reportesSerializadosPMI.data
            }
        })
    
    def delete(self, request,id_reporte):
        reporte = Reporte.objects.filter(id="id_reporte")
        reporte.delete()
        return Response({"eliminado_id" : id_reporte})

    def reportePdf(self, request, *args, **kwargs):
        model = Reporte
        template_name = "webapp/reporte_UPCI.html"
        context_object_name = 'reportes'
#Pruebas para el envio de reporte pdf generado via email
class ReporteUpciPDFViewSet4 (ListView):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor']
    
    @staticmethod
    def get(request):        
        reportes = Reporte.objects.filter(id=116)#49
        format_time = "%d-%m-%Y"
        actor = Reporte.objects.get(id=116)
        data = {
            'reportes': reportes,
        }
        template_name = "webapp/reporte_UPCI.html"
        pdf = render_to_pdf (template_name, data)
        file_name = 'Reporte_%s_%s.pdf' %(actor.actor.sigla, actor.modificado.strftime(format_time))
        #return render(request, template_name, data)
        
        # modificado
        # return  HttpResponse(pdf, content_type='application/pdf')        

        #response['Content-Disposition'] = 'inline; filename=' + file_name
        #return response
        contexto = {
            "nombre_usuario" : "Seba",
            "tipo_entrega" : "verificador",
        }
        # envío de correo al colaborador que subió la entrega
        #html_content = loader.render_to_string("webapp/correo_Finalizado_colaborador.html", contexto)
        
        subject = "Prueba envio adjunto Reporte"
        body = "Entrega reporte enviado"
        from_email = "colabora@uaysen.cl"
        recipient_list = ['sebastiansaezmansilla@gmail.com']

        #Open PDF file in binary mode
        #with open(pdf, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        #    part = MIMEBase("application", "octet-stream")
        #    part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        #encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        #part.add_header("Content-Disposition", f"attachment; filename= {file_name}",)
        part = (file_name, pdf, 'application/pdf')
        #async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=pdf)
        return  HttpResponse(pdf, content_type='application/pdf')
        

class ReporteUpciPDFViewSet (ListView):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor']
    
    @staticmethod
    def get(request, id_reporte):        
        reportes = Reporte.objects.filter(id=id_reporte)#49
        actor = Reporte.objects.get(id=id_reporte)
        format_time = "%d-%m-%Y"
        fecha = actor.modificado.strftime(format_time)
        data = {
            'reportes': reportes,
        }
        template_name = "webapp/reporte_UPCI.html"
        pdf = render_to_pdf (template_name, data)
        file_name = 'Reporte_%s_%s.pdf' %(actor.actor.sigla, fecha)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + file_name
        return response

class ReporteUpciPmiPDFViewSet (ListView):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor']
    
    @staticmethod
    def get(request, id_reporte):        
        reportes = Reporte.objects.filter(id=id_reporte)#49
        actor = Reporte.objects.get(id=id_reporte)
        format_time = "%d-%m-%Y"
        fecha = actor.modificado.strftime(format_time)
        data = {
            'reportes': reportes,
        }
        template_name = "webapp/reporte_UPCI_PMI.html"
        pdf = render_to_pdf (template_name, data)
        file_name = 'Reporte_PMI_%s_%s.pdf' %(actor.actor.sigla, fecha)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + file_name
        return response

class ReporteUpciPmiPDFViewSet4 (ListView):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor']
    
    @staticmethod
    def get(request):        
        reportes = Reporte.objects.filter(id=116)#49
        data = {
            'reportes': reportes,
        }
        template_name = "webapp/reporte_UPCI_PMI.html"
        pdf = render_to_pdf (template_name, data)
        #file_name = 'Reporte_%s_%s.pdf' %(actor.actor.sigla, fecha)
        #return render(request, template_name, data)
        return  HttpResponse(pdf, content_type='application/pdf')
        #response['Content-Disposition'] = 'inline; filename=' + file_name
        #return response

class EditaVerificadorViewSet(viewsets.ModelViewSet):
    #queryset = Verificador.objects.all().filter(estado='Borrador')
    queryset = Verificador.objects.all().order_by('-modificado')
    serializer_class = VerificadorSerializer
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['patch', 'get']

    @action(detail=False, methods=['patch','get'])
    def verificadoresRechazados(self, request):
        datosRequest = request.data     
        verificador = Verificador.objects.filter(usuario=request.user)
        verificador = Verificador.objects 
        serializer = self.serializer_class(instance=verificador, data=datosRequest, partial = True)

        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse({'verificadores_borradores' :
                {
                'verificadores' : serializer.data
                }
            })
        else:            
            return Response(serializer.errors)            

class EditaProductoViewSet (viewsets.ModelViewSet):
    #queryset = Producto.objects.all().filter(estado='Borrador')
    queryset = Producto.objects.all().order_by('-modificado')
    serializer_class = ProductoSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['patch', 'get']

    @action(detail=False, methods=['patch','get'])
    def ProductosRechazados(self, request):
        datosRequest = request.data     
        producto = Producto.objects 
        serializer = self.serializer_class(instance=producto, data=datosRequest, partial = True)

        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse({'productos_borradores' :
                {
                'productos' : serializer.data
                }
            })
        else:
            return Response(serializer.errors) 

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all().order_by('-id')
    serializer_class = RolSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo','actor','accion']

    @action(detail=False, methods=['get'], url_path=r'rolPorRol/(?P<tipo>[^/.]+)/(?P<origen>[^/.]+)')
    def rolPorRol(self, request, tipo, origen='POA', *args, **kwargs):
        perfilUsuario = getPerfilUsuario(request)
        accionesPorRol = {}
        listaAcciones = []
        origen_anterior = ""

        if tipo == "Informado":
            #roles = Rol.objects.filter(actor__in=validaDependencia(perfilUsuario.actor), tipo=tipo).order_by('accion__origen')
            #roles = Rol.objects.filter(actor__in=validaDependencia(perfilUsuario.actor), tipo=tipo  or tipo='Responsable').order_by('accion__origen')
            #roles = Rol.objects.filter(actor__in=validaDependencia(perfilUsuario.actor), tipo__in=[tipo, 'Responsable']).order_by('accion__origen')
            roles = Rol.objects.filter(actor__in=validaDependencia(perfilUsuario.actor), tipo=tipo).order_by('accion__origen')
        else:            
            roles = Rol.objects.filter(actor=perfilUsuario.actor, tipo=tipo).order_by('accion__origen')
        
        #roles = Rol.objects.filter(actor=perfilUsuario.actor, tipo=tipo, accion__origen=origen)
        
        serializer = self.get_serializer(roles, many=True)
        
        if len(serializer.data) > 0:
            origen = serializer.data[0]['accion']['origen']        
        else:
            return Response(accionesPorRol)

        for rol in serializer.data:                
            if origen == rol['accion']['origen']:                
                #listaAcciones.append(rol['accion'])
                listaAcciones.append(rol)
            else:                                
                if(rol['accion']['origen'] == "POA"):
                    origen_anterior = origen
                    if(rol['accion']['proyecto'] is None):                        
                        origen = "TRANSVERSAL"
                    else:
                        origen = "URY"
                else:
                    origen_anterior = origen
                    origen = rol['accion']['origen']                
                if origen != origen_anterior:                    
                    listaAcciones = []
                    listaAcciones.append(rol)
                else:
                    listaAcciones.append(rol)                
        
            accionesPorRol[origen] = listaAcciones    
        #return Response(serializer.data)
        return Response(accionesPorRol)
    
    @action(detail=False, methods=['get'], url_path=r'rolResponsable/(?P<id_actor>[^/.]+)')
    def rolResponsable(self, request, id_actor, *args, **kwargs):              
        if id_actor != "0":
            roles = Rol.objects.filter(actor=id_actor, tipo ="Responsable", accion__origen="POA")
        else:
            roles = Rol.objects.filter(tipo ="Responsable", accion__origen="POA")
            
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'rolResponsablePMI/(?P<id_actor>[^/.]+)')
    def rolResponsablePMI(self, request, id_actor, *args, **kwargs):
        if id_actor != "0":
            roles = Rol.objects.filter(actor=id_actor, tipo ="Responsable", accion__origen="PMI")
        else:
            roles = Rol.objects.filter(tipo ="Responsable", accion__origen="PMI")
            
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data)

class EstrategiaViewSet(viewsets.ModelViewSet):
    queryset = Estrategia.objects.all()
    serializer_class = EstrategiasSimpleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['periodo']
    http_method_names = ['get']

#########################################################
# Sección BACKEND workflow de las entregas (entregables)
#########################################################
@api_view(['POST'])
def entregableEnviaALider(request):
    '''
    evento del workflow donde un colaborador envía una entrega
    a su encargado de unidad (líder). Consideraciones (a validar):
     - la entrega debiese estar en estado "borrador"
     - la entrega es de tipo verificador o producto
     - solo el colaborador puede enviar al líder sus propias entregas
    probablemente, sea una tarea previamente rechazada
    '''
    datosRequest = request.data

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        if verificador.usuario.id != request.user.id :
            raise PermissionDenied()
        verificador.envia_a_lider()
        verificador.save()
        serializer = VerificadorDepthSerializer(verificador)
        return Response(serializer.data)

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        if producto.usuario.id != request.user.id :
            raise PermissionDenied()
        producto.envia_a_lider()
        producto.save()
        serializer = ProductoDepthSerializer(producto)
        return Response(serializer.data)
        
    else :
        raise PermissionDenied()

@api_view(['POST'])
def entregableLiderDaVistoBueno(request) :
    '''
    evento del workflow donde un(a) líder de unidad da el visto
    bueno para que la entrega sea revisada por UPCI.
    Consideraciones (a validar):
     - la entrega debiese estar en estado "enviado al lider"
     - la entrega es de tipo verificador o producto
     - solo el **encargado de la unidad responsable** de la entrega
     tiene permitido dar este visto bueno
    '''
    datosRequest = request.data
    perfilUsuario = getPerfilUsuario(request)

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        # TODO: condicion incompleta, debe ser encargado de la
        # unidad responsable de la accion de la entrega
        if not perfilUsuario.es_encargado :
            raise PermissionDenied()
        verificador.envia_a_UPCI()
        verificador.save()
        serializer = VerificadorDepthSerializer(verificador)
        return Response(serializer.data)

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        # TODO: condicion incompleta, debe ser encargado de la
        # unidad responsable de la accion de la entrega
        if not perfilUsuario.es_encargado :
            raise PermissionDenied()
        producto.envia_a_UPCI()
        producto.save()
        serializer = ProductoDepthSerializer(producto)
        return Response(serializer.data)
        
    else :
        raise PermissionDenied()

@api_view(['POST'])
def entregableUPCIDaVistoBueno(request) :
    '''
    evento del workflow donde un(a) líder de unidad da el visto
    bueno para que la entrega sea revisada por UPCI.
    Consideraciones (a validar):
     - la entrega debiese estar en estado "enviado al lider"
     - la entrega es de tipo verificador o producto
     - solo el **encargado de la unidad responsable** de la entrega
     tiene permitido dar este visto bueno
    '''
    datosRequest = request.data
    perfilUsuario = getPerfilUsuario(request)

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        if not perfilUsuario.es_analistaUPCI :
            raise PermissionDenied()
        verificador.acepta_UPCI()
        verificador.save()
        serializer = VerificadorDepthSerializer(verificador)
        return Response(serializer.data)

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        if not perfilUsuario.es_analistaUPCI :
            raise PermissionDenied()
        producto.acepta_UPCI()
        producto.save()
        serializer = ProductoDepthSerializer(producto)
        return Response(serializer.data)
        
    else :
        raise PermissionDenied()

@api_view(['POST'])
def entregableLiderRechaza(request) :
    '''
    evento del workflow donde un(a) líder de unidad rechaza
    y da feedback de la entrega
    '''
    datosRequest = request.data
    perfilUsuario = getPerfilUsuario(request)

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        # TODO: condicion incompleta, debe ser encargado de la
        # unidad responsable de la accion de la entrega
        if not perfilUsuario.es_encargado :
            raise PermissionDenied()
        verificador.rechaza_lider(datosRequest['retroalimentacion'])
        verificador.save()
        RetroEntrega.objects.create(
            usuario=request.user,
            verificador=verificador,
            retroalimentacion=datosRequest['retroalimentacion']
        )
        serializer = VerificadorDepthSerializer(verificador)
        return Response(serializer.data)

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        # TODO: condicion incompleta, debe ser encargado de la
        # unidad responsable de la accion de la entrega
        if not perfilUsuario.es_encargado :
            raise PermissionDenied()
        producto.rechaza_lider(datosRequest['retroalimentacion'])
        producto.save()
        RetroEntrega.objects.create(
            usuario=request.user,
            producto=producto,
            retroalimentacion=datosRequest['retroalimentacion']
        )
        serializer = ProductoDepthSerializer(producto)
        return Response(serializer.data)
        
    else :
        raise PermissionDenied()

@api_view(['POST'])
def entregableUPCIRechaza(request) :
    '''
    evento del workflow donde UPCI rechaza y da retroalimentación
    de la entrega
    '''
    datosRequest = request.data
    perfilUsuario = getPerfilUsuario(request)

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        if not perfilUsuario.es_analistaUPCI :
            raise PermissionDenied()
        verificador.rechazado_UPCI(datosRequest['retroalimentacion'])
        verificador.save()
        RetroEntrega.objects.create(
            usuario=request.user,
            verificador=verificador,
            retroalimentacion=datosRequest['retroalimentacion']
        )
        serializer = VerificadorDepthSerializer(verificador)
        return Response(serializer.data)

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        if not perfilUsuario.es_analistaUPCI :
            raise PermissionDenied()
        producto.rechazado_UPCI(datosRequest['retroalimentacion'])
        producto.save()
        RetroEntrega.objects.create(
            usuario=request.user,
            producto=producto,
            retroalimentacion=datosRequest['retroalimentacion']
        )
        serializer = ProductoDepthSerializer(producto)
        return Response(serializer.data)
        
    else :
        raise PermissionDenied()

@api_view(['POST'])
def entregableDescarta(request) :
    '''
    evento del workflow donde un(a) líder de unidad da el visto
    bueno para que la entrega sea revisada por UPCI.
    Consideraciones (a validar):
     - la entrega debiese estar en estado "enviado al lider"
     - la entrega es de tipo verificador o producto
     - solo el **encargado de la unidad responsable** de la entrega
     tiene permitido dar este visto bueno
    '''
    datosRequest = request.data

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        if verificador.usuario.id != request.user.id :
            raise PermissionDenied()
        verificador.delete()
        return Response({"eliminado_id" : datosRequest['entrega_id'], "eliminado_tipo" : datosRequest['entrega_tipo']})

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        if producto.usuario.id != request.user.id :
            raise PermissionDenied()
        producto.delete()
        return Response({"eliminado_id" : datosRequest['entrega_id'], "eliminado_tipo" : datosRequest['entrega_tipo']})
    else :
        raise PermissionDenied()
#########################################################
# FIN Sección BACKEND workflow de las entregas
#########################################################

@api_view(['GET'])
def accionesFiltradas(request) :
    actor = request.query_params['actor']
    rol = request.query_params['rol']
    tipo = request.query_params['tipo']
    anio = request.query_params['anio']
    origen = request.query_params['origen']

    filtro = Q()
    dict_filtros = {}
    
    if actor != "Todos" :
        dict_filtros['rol__actor__id'] = actor
    
    if rol != "Todos" :
        dict_filtros['rol__tipo'] = rol

    if tipo != "Todos" :
        dict_filtros['tipo'] = tipo

    if anio != "Todos" :
        dict_filtros['anio'] = anio
    
    if origen != "Todos" :
        dict_filtros['origen'] = origen
    
    if anio == "2022":
        if origen == "URY":
            #dict_filtros['proyecto__isnull'] = False
            filtro |= Q( proyecto__isnull=False, origen ="POA")
            dict_filtros.pop('origen', None)
            
        if origen == "TRANSVERSAL":
            filtro |= Q( proyecto__isnull=True, origen ="POA")
            dict_filtros.pop('origen', None)
            #dict_filtros['proyecto__isnull'] = True

    if anio == "Todos":
        if origen == "URY":
            filtro |= Q(origen="URY", anio__gte=2022) | Q(proyecto__isnull=False, anio=2022)
            dict_filtros.pop('origen', None)
        if origen == "TRANSVERSAL":
            filtro |= Q(origen="TRANSVERSAL", anio__gte=2022) | Q( proyecto__isnull=True, anio=2022)
            dict_filtros.pop('origen', None)


    for item in dict_filtros:
        filtro &= Q(**{item:dict_filtros[item]})    
    qs = Accion.objects.filter(filtro)
    serializer = AccionSimpleSerializer(qs, many=True)

    return Response(serializer.data)

# solo para razones de testing:
def permission_denied_view(request):
    raise PermissionDenied()

# requests de uso interno
# 404
def cuatrocientoscuatro(request, exception=None):
    context = {'state': 'ok'}
    return render(request, 'webapp/404.html', context)

def render_to_pdf(template_reporte, context_dict={}):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

    template = get_template(template_reporte)
    html = template.render(context_dict)

    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)

    if pisa_status.err:
        return HttpResponse("some problem with pdf")
    return response

def validaDependencia(actor):    
    dependencia = actor.dependencia    
    actores = [actor]
    while dependencia is not None:
        #if dependencia.es_direccion:
        if dependencia.dependencia is None:                      
            actores.append(dependencia)
            return actores
            #return obtenerActoresDependientes(dependencia)
        
        dependencia = dependencia.dependencia
    return None

def obtenerActoresDependientes(actor):
    actores = []
    cola_actores = [actor]
    while cola_actores:
        actual = cola_actores.pop(0)
        actores.append(actual)
        dependientes = Actor.objects.filter(dependencia=actual)
        for dependiente in dependientes:
            cola_actores.append(dependiente)
    return actores


def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = STATIC_URL        # Typically /static/
                    sRoot = STATIC_ROOT      # Typically /home/userX/project_static/

                    if uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl)
                    )
            return path
