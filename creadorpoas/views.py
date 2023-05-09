from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Proto_Accion, Proto_Hito, \
    Proto_MDV, Proto_CriterioMDV, Proto_Funcion, Proto_Indicador, \
    Proto_Presupuesto, Proto_Colaborador, CtaContable
from webapp.models import Estrategia
from .serializers import *
from rest_framework.decorators import action

class Proto_Accion_ViewSet(viewsets.ModelViewSet) :
    queryset = Proto_Accion.objects.all()
    serializer_class = Proto_Accion_Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_uaysen']
    http_method_names = ['get', 'post', 'patch']

class Proto_Accion_Depth_ViewSet(viewsets.ModelViewSet) :
    queryset = Proto_Accion.objects.all()
    serializer_class = Proto_Accion_Depth_Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    @action(detail=False, methods=['patch'])
    def agregaEstrategia(self, request):
        datosRequest = request.data
        accion = get_object_or_404(Proto_Accion, pk=datosRequest['id_accion'])
        estrategia = get_object_or_404(Estrategia, pk=datosRequest['id_estrategia'])
        if not accion.estrategias.filter(pk=estrategia.pk).exists() :
            accion.estrategias.add(estrategia)
            accion.save()
        objSerializado = self.get_serializer(accion, many=False)
        return JsonResponse(objSerializado.data)

    @action(detail=False, methods=['patch'])
    def quitaEstrategia(self, request):
        datosRequest = request.data
        accion = get_object_or_404(Proto_Accion, pk=datosRequest['id_accion'])
        estrategia = get_object_or_404(Estrategia, pk=datosRequest['id_estrategia'])
        if accion.estrategias.filter(pk=estrategia.pk).exists() :
            accion.estrategias.remove(estrategia)
            accion.save()
        objSerializado = self.get_serializer(accion, many=False)
        return JsonResponse(objSerializado.data)

class Proto_Hito_ViewSet(viewsets.ModelViewSet) :
    queryset = Proto_Hito.objects.all()
    serializer_class = Proto_Hito_Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre']

class Proto_MDV_ViewSet(viewsets.ModelViewSet) :
    queryset = Proto_MDV.objects.all()
    serializer_class = Proto_MDV_Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre']

class Proto_CriterioMDV_ViewSet(viewsets.ModelViewSet) :
    queryset = Proto_CriterioMDV.objects.all()
    serializer_class = Proto_CriterioMDV_Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mdv']

class Proto_Funcion_ViewSet(viewsets.ModelViewSet) :
    queryset = Proto_Funcion.objects.all()
    serializer_class = Proto_Funcion_Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre']

class Proto_Indicador_ViewSet(viewsets.ModelViewSet) :
    queryset = Proto_Indicador.objects.all()
    serializer_class = Proto_Indicador_Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre']

class Proto_Presupuesto_ViewSet(viewsets.ModelViewSet) :
    queryset = Proto_Presupuesto.objects.all()
    serializer_class = Proto_Presupuesto_Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['accion']

class Proto_Colaborador_ViewSet(viewsets.ModelViewSet) :
    queryset = Proto_Colaborador.objects.all()
    serializer_class = Proto_Colaborador_Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['accion']

class CtaContable_ViewSet(viewsets.ModelViewSet) :
    queryset = CtaContable.objects.all()
    serializer_class = CtaContable_Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_uaysen']
