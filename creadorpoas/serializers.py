from .models import Proto_Accion, Proto_Hito, \
    Proto_MDV, Proto_CriterioMDV, Proto_Funcion, Proto_Indicador, \
    Proto_Presupuesto, Proto_Colaborador, CtaContable
from rest_framework import serializers

class Proto_Accion_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Proto_Accion
        fields = ["id", "creador", "unidad", "creado", "modificado", "id_uaysen", "anio", "proyecto", "titulo", "objetivo", "tipo"]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["num_estrategias"] = len(instance.estrategias.all())
        data["num_hitos"] = len(instance.proto_hito_set.all())
        data["num_mdvs"] = len(instance.proto_mdv_set.all())
        data["num_funciones"] = len(instance.proto_funcion_set.all())
        data["num_presupuestos"] = len(instance.proto_presupuesto_set.all())
        data["num_colaboradores"] = len(instance.proto_colaborador_set.all())
        data["proyecto"] = data["proyecto"] if data["proyecto"] else "Ninguno"
        data["modificacion"] = instance.modificado.astimezone().strftime("%d-%m-%Y, a las %H:%M:%S")
        data["creacion"] = instance.creado.astimezone().strftime("%d-%m-%Y, a las %H:%M:%S")
        return data

class Proto_Hito_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Proto_Hito
        fields = '__all__'

class Proto_MDV_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Proto_MDV
        fields = '__all__'

class Proto_CriterioMDV_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Proto_CriterioMDV
        fields = '__all__'

class Proto_Funcion_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Proto_Funcion
        fields = '__all__'

class Proto_Indicador_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Proto_Indicador
        fields = '__all__'

class Proto_Presupuesto_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Proto_Presupuesto
        fields = '__all__'

class Proto_Colaborador_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Proto_Colaborador
        fields = '__all__'

class CtaContable_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CtaContable
        fields = '__all__'

class Proto_Accion_Depth_Serializer(serializers.ModelSerializer):
    proto_hito_set = Proto_Hito_Serializer(read_only=True, many=True)
    proto_funcion_set = Proto_Funcion_Serializer(read_only=True, many=True)
    proto_mdv_set = Proto_MDV_Serializer(read_only=True, many=True)
    
    class Meta:
        model = Proto_Accion
        fields = ["id", "id_uaysen", "anio", "proyecto", "titulo", "objetivo", "tipo", "estrategias", "proto_hito_set", "proto_funcion_set", "proto_mdv_set"]
        depth = 2

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["proyecto"] = data["proyecto"] if data["proyecto"] else "Ninguno"
        data["modificacion"] = instance.modificado.astimezone().strftime("%d-%m-%Y, a las %H:%M:%S")
        data["creacion"] = instance.creado.astimezone().strftime("%d-%m-%Y, a las %H:%M:%S")
        return data