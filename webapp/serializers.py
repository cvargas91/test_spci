from pickle import TRUE
from django.contrib.auth.models import User, Group
from .models import Accion, Actor, Rol, Producto, Verificador,\
    RetroEntrega, MDV, Hito, Funcion, Indicador, Estrategia, Reporte,\
    ReporteAccion, ReporteFuncion, ReporteHito, Dimension
from rest_framework import serializers,fields
from drf_writable_nested.serializers import WritableNestedModelSerializer
from pytz import timezone
from collections import OrderedDict
from spci.settings import TIME_ZONE

class HitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hito
        fields = '__all__'

class IndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicador
        fields = '__all__'

class FuncionSerializer(serializers.ModelSerializer):
    indicador_set = IndicadorSerializer(read_only=True, many=True)
    class Meta:
        model = Funcion
        fields = ['accion', 'nombre', 'dirGoogle', 'indicador_set']

### Elementos del sistema subidos por los usuarios
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'usuario', 'mdv', 'hitos', 'descripcion', 'estado', 'adjuntos', 'modificado', 'creado']
        
    def update(self, instance, validate_data):
        instance.mdv = validate_data.get('mdv', instance.mdv)        
        instance.hitos.set(validate_data.get('hitos', instance.hitos))
        instance.descripcion = validate_data.get('descripcion', instance.descripcion)
        instance.adjuntos = validate_data.get('adjuntos', instance.adjuntos)
        instance.modificado = validate_data.get('modificado', instance.modificado)
        instance.save()
        return instance

class ProductoDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'usuario', 'mdv', 'hitos', 'descripcion', 'estado', 'adjuntos', 'modificado', 'creado']
        depth = 3

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["fecha_creacion"] = instance.creado.strftime('%d/%m/%Y')
        return data

class VerificadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificador
        fields = ['id', 'usuario', 'indicador', 'valor', 'descripcion', 'adjuntos', 'estado', 'modificado', 'creado']
    
    def update(self, instance, validated_data):
        instance.indicador = validated_data.get('indicador', instance.indicador)
        instance.valor = validated_data.get('valor', instance.valor)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.adjuntos = validated_data.get('adjuntos', instance.adjuntos)
        instance.modificado = validated_data.get('modificado', instance.modificado)
        instance.save()
        return instance
    

class VerificadorDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificador
        fields = ['id', 'usuario', 'indicador', 'valor', 'descripcion', 'adjuntos', 'estado', 'modificado', 'creado']
        depth = 3

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["fecha_creacion"] = instance.creado.strftime('%d/%m/%Y')
        return data
### (FIN) Elementos del sistema subidos por los usuarios

class RetroEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroEntrega
        fields = ['id', 'usuario', 'producto', 'verificador', 'retroalimentacion']
    
    def to_representation (self, instance):
        data = super().to_representation(instance)
        new_format = "%d/%m/%Y - %H:%M:%S"
        new_date_modificado = instance.modificado.astimezone(timezone(TIME_ZONE))
        new_date_creado     = instance.creado.astimezone(timezone(TIME_ZONE))
        data["creado"] = new_date_creado.strftime(new_format)
        data["modificado"] = new_date_modificado.strftime(new_format)
        return data

class ReporteFuncionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteFuncion
        fields =['id','id_tactica','funcion','indicador','comentario_cumplimiento']

class ReporteHitoSerializer(serializers.ModelSerializer):
    #mdvs = MDVSerializer(many=True)
    #hitos = HitoSerializer(many=True)
    class Meta:
        model = ReporteHito
        fields = ['id','id_tactica','mdvs','hito','indicador','indicador_logro','justificacion_contingencia','reporte_justificacion_contingencia','comentario_cumplimiento']

class ReporteAccionSerializer(serializers.ModelSerializer):
    reporte_funciones = ReporteFuncionSerializer(many=True)
    reporte_hitos = ReporteHitoSerializer(many=True)
    
    class Meta:
        model = ReporteAccion
        fields = ['id','accion','estado_ejecucion','justificacion_contingencia','reporte_justificacion_contingencia','indicador','indicador_logro','reporte_funciones','reporte_hitos']


class ReporteSerializer(serializers.ModelSerializer):
    reporte_acciones = ReporteAccionSerializer(many=True)

    class Meta:
        model = Reporte
        fields = ['id', 'usuario', 'actor', 'estado', 'recomendacion','tipo','enviado','reporte_acciones','creado','modificado']    

    def create(self, validated_data):
        reporte_acciones = validated_data.pop('reporte_acciones')
        reporte_data = Reporte.objects.create(**validated_data)

        for reporte_accion in reporte_acciones:
            funciones_data = reporte_accion.pop('reporte_funciones')
            hitos_data = reporte_accion.pop('reporte_hitos')

            reporte_accion_data=ReporteAccion.objects.create(detalle_reporte=reporte_data,**reporte_accion)
            
            for funcion_data in funciones_data:
                ReporteFuncion.objects.create(dependencia=reporte_accion_data,**funcion_data)            
            for hito in hitos_data:
                #id_hitos = hito.pop('hitos')
                id_mdvs = hito.pop('mdvs')
                repo_hito = ReporteHito.objects.create(dependencia=reporte_accion_data, **hito)
                #for id_hito in id_hitos:
                #    repo_hito.hitos.add(id_hito)
                for id_mdv in id_mdvs:
                    repo_hito.mdvs.add(id_mdv)
                    
        return reporte_data
        
    def update(self, instance ,validated_data):
        
        reporte_acciones = validated_data.pop('reporte_acciones')
        instance.estado = validated_data.get('estado', instance.estado)
        instance.enviado = validated_data.get('enviado', instance.enviado)
        instance.recomendacion = validated_data.get('recomendacion', instance.recomendacion)
        instance.modificado = validated_data.get('modificado', instance.modificado)
        instance.tipo = validated_data.get('tipo', instance.tipo)
        reporte_acciones_data = (instance.reporte_acciones).all()
        reporte_acciones_data = list(reporte_acciones_data)
        #instance.reporte_acciones = validated_data.get('reporte_acciones', instance.reporte_acciones)
        instance.save()
        
        reporte_accion_nuevos_id = []
        
        #se agregan o modifican nuevos reportes de acciones
        for reporte_accion in reporte_acciones:
            funciones_data = reporte_accion.pop('reporte_funciones')
            hitos_data = reporte_accion.pop('reporte_hitos')

            if "id" in reporte_accion.keys():
                if ReporteAccion.objects.filter(id=reporte_accion['id']).exists():
                    reporte_accion_instance = ReporteAccion.objects.get(id=reporte_accion['id'])
                    reporte_accion_instance.detalle_reporte = reporte_accion.get('detalle_reporte', reporte_accion_instance.detalle_reporte)
                    #reporte_accion_instance.mdvs.append(reporte_accion.get('mdvs', reporte_accion_instance.mdvs))
                    reporte_accion_instance.estado_ejecucion = reporte_accion.get('estado_ejecucion', reporte_accion_instance.estado_ejecucion)
                    reporte_accion_instance.justificacion_contingencia = reporte_accion.get('justificacion_contingencia', reporte_accion_instance.justificacion_contingencia)
                    reporte_accion_instance.reporte_justificacion_contingencia = reporte_accion.get('reporte_justificacion_contingencia', reporte_accion_instance.reporte_justificacion_contingencia)
                    for funcion_data in funciones_data:
                        ReporteFuncion.objects.create(dependencia=reporte_accion_instance,**funcion_data)            
                    for hito in hitos_data:
                        #id_hitos = hito.pop('hitos')
                        id_mdvs = hito.pop('mdvs')
                        repo_hito = ReporteHito.objects.create(dependencia=reporte_accion_instance, **hito)
                        #for id_hito in id_hitos:
                        #    repo_hito.hitos.add(id_hito)
                        for id_mdv in id_mdvs:
                            repo_hito.mdvs.add(id_mdv)

                    reporte_accion_instance.save()
                    reporte_accion_nuevos_id.append(reporte_accion_instance.id)
                else:
                    continue
            else:
                reporte_accion_instance = ReporteAccion.objects.create(detalle_reporte=instance, **reporte_accion)
                for funcion_data in funciones_data:
                    ReporteFuncion.objects.create(dependencia=reporte_accion_instance,**funcion_data)            
                for hito in hitos_data:
                #     id_hitos = hito.pop('hitos')
                    id_mdvs = hito.pop('mdvs')
                    repo_hito = ReporteHito.objects.create(dependencia=reporte_accion_instance, **hito)
                    #for id_hito in id_hitos:
                    #    repo_hito.hitos.add(id_hito)

                    for id_mdv in id_mdvs:
                        repo_hito.mdvs.add(id_mdv)
                    #ReporteHito.objects.create(dependencia=reporte_accion_instance, **hito)
                reporte_accion_nuevos_id.append(reporte_accion_instance.id)

        #se eliminan reportes de acciones que no esten en el request
        for reporte_accion_id in instance.reporte_acciones.values_list('id', flat=True):
            if reporte_accion_id not in reporte_accion_nuevos_id:
                ReporteAccion.objects.filter(pk=reporte_accion_id).delete()
        
        return instance

    
    def to_representation (self, instance):
        data = super().to_representation(instance)
        new_format = "%d/%m/%Y - %H:%M:%S"
        new_date_modificado = instance.modificado.astimezone(timezone(TIME_ZONE))
        new_date_creado     = instance.creado.astimezone(timezone(TIME_ZONE))
        data["creado"] = new_date_creado.strftime(new_format)
        data["modificado"] = new_date_modificado.strftime(new_format)
        return data

class ActualizaVerificadorSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.mdv = validated_data.get('mdv', instance.mdv)
        instance.hitos = validated_data.get('hitos', instance.hitos)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.adjuntos = validated_data.get('adjuntos', instance.adjuntos)
        instance.modificado = serializers.DateTimeField(auto_now=True)
        instance.save()
        return instance

    class Meta:
        model = Verificador
        fields = ['id', 'usuario', 'mdv', 'hitos', 'descripcion', 'estado', 'adjuntos', 'modificado', 'creado']

class ActualizaProductoSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.mdv = validated_data.get('mdv', instance.mdv)
        instance.hitos = validated_data.get('hitos', instance.hitos)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.adjuntos = validated_data.get('adjuntos', instance.adjuntos)
        instance.modificado = serializers.DateTimeField(auto_now=True)
        instance.save()
        return instance

    class Meta:
        model = Producto
        fields = ['id', 'usuario', 'mdv', 'hitos', 'descripcion', 'estado', 'adjuntos', 'modificado', 'creado']

class RolSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Rol
        fields = ['id', 'accion', 'actor', 'tipo']
        depth = 3

class RolSimpleSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Rol
        fields = ['id', 'actor', 'tipo']
        depth = 1

class EstrategiasSimpleSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Estrategia
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["value"] = instance.id
        data["label"] = instance.id_uaysen
        return data

class AccionSerializer(serializers.ModelSerializer):
    rol_set = RolSimpleSerializer(read_only=True, many=True)
    class Meta:
        model = Accion
        fields = ['id', 'titulo', 'id_uaysen', \
            'objetivo', 'tipo', 'anio', 'proyecto', \
            'estrategias','dimensiones' ,'rol_set', 'dirGoogle',
            'presupuesto','origen']
        depth = 1

class AccionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accion
        fields = ['id', 'titulo', 'id_uaysen', \
            'objetivo', 'tipo', 'anio', 'proyecto', \
            'estrategias', 'dimensiones','presupuesto','origen']
        depth = 1

class MDVSerializer(serializers.ModelSerializer):
    class Meta:
        model = MDV
        fields = ['id', 'accion', 'nombre', 'dirGoogle']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["value"] = instance.id
        data["label"] = instance.nombre
        return data

class ActorSerializer(serializers.ModelSerializer):
    #rol_set = RolSimpleSerializer(read_only=True, many=True)
    class Meta:
        model = Actor
        fields = ['id', 'nombre', 'id_uaysen', \
            'sigla', 'cai', 'es_area', 'categoria', \
            'dependencia', 'es_direccion']
        depth = 1

class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = ['id', 'nombre','texto_ley']
        depth = 1