from django.contrib import admin
from .models import Proto_Accion, Proto_Hito, \
    Proto_MDV, Proto_CriterioMDV, Proto_Funcion, Proto_Indicador, \
    Proto_Presupuesto, Proto_Colaborador, CtaContable

@admin.register(Proto_Accion)
class Proto_Accion_Admin(admin.ModelAdmin) :
    actions = None

@admin.register(Proto_Hito)
class Proto_Hito_Admin(admin.ModelAdmin) :
    actions = None

@admin.register(Proto_MDV)
class Proto_MDV_Admin(admin.ModelAdmin) :
    actions = None

@admin.register(Proto_CriterioMDV)
class Proto_CriterioMDV_Admin(admin.ModelAdmin) :
    actions = None

@admin.register(Proto_Funcion)
class Proto_Funcion_Admin(admin.ModelAdmin) :
    actions = None

@admin.register(Proto_Indicador)
class Proto_Indicador_Admin(admin.ModelAdmin) :
    actions = None

@admin.register(Proto_Presupuesto)
class Proto_Presupuesto_Admin(admin.ModelAdmin) :
    actions = None

@admin.register(Proto_Colaborador)
class Proto_Colaborador_Admin(admin.ModelAdmin) :
    actions = None

@admin.register(CtaContable)
class CtaContable_Admin(admin.ModelAdmin) :
    actions = None
