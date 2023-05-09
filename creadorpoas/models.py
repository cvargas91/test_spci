from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from webapp.models import Actor, nombresRol

PREFIJO_PROTO = '[PROTO] '
MAX_LENGTH = 250
MIDDLE_LENGTH = 100
SHORT_LENGTH = 10

carreras = [
    ('Enfermería', 'Enfermería'),
    ('Obstetricia', 'Obstetricia'),
    ('Ingeniería Civil Industrial', 'Ingeniería Civil Industrial'),
    ('Ingeniería Civil Computación', 'Ingeniería Civil Computación'),
    ('Trabajo Social', 'Trabajo Social'),
    ('Psicología', 'Psicología'),
    ('Ingeniería Forestal', 'Ingeniería Forestal'),
    ('Agronomía', 'Agronomía'),
]

tiposAccion = [
    ('Misional', 'Misional'),
    ('Desarrollo', 'Desarrollo'),
]

tiposTactica = [
    ('Función', 'Función'),
    ('Hito', 'Hito')
]

anios = [
    (2017, 2017),
    (2018, 2018),
    (2019, 2019),
    (2020, 2020),
    (2021, 2021),
    (2022, 2022),
    (2023, 2023),
    (2024, 2024),
    (2025, 2025),
    (2026, 2026),
    (2027, 2027),
    (2028, 2028),
    (2029, 2029),
    (2030, 2030),
]

class Proto_Accion(models.Model) :
    # to-do:
    # - relacionar con el usuario que creó la proto-accion
    # - relacionar con el actor (unidad) del usuario creador
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Usuario que creó la propuesta de acción')
    unidad = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Unidad a la que pertenece la propuesta de acción')
    estrategias = models.ManyToManyField('webapp.Estrategia', blank=True)
    id_uaysen = models.CharField(max_length=MAX_LENGTH, verbose_name='Identificador interno', blank=True)
    proyecto = models.CharField(max_length=MAX_LENGTH, null=True, verbose_name='Proyecto URY')
    anio = models.PositiveIntegerField(choices=anios, verbose_name='Año', default=2023, blank=True)
    titulo = models.TextField(verbose_name='Título')
    objetivo = models.TextField(verbose_name='Objetivo')
    tipo = models.CharField(max_length=MAX_LENGTH, choices=tiposAccion, verbose_name='Tipo de acción')
    presupuesto = models.PositiveIntegerField(verbose_name='Presupuesto en pesos chilenos', null=True)
    modificado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = PREFIJO_PROTO + "Acción"
        verbose_name_plural = PREFIJO_PROTO + "Acciones"

    def __str__(self):
        return '{}: {}'.format(self.id_uaysen, self.titulo)

    def save(self, *args, **kwargs):
        if not self.id_uaysen :
            idPrefijo = self.unidad.sigla
            nuevoId = 1
            if self.unidad.dependencia :
                idPrefijo = self.unidad.dependencia.sigla
            numeritos = []
            for accion in Proto_Accion.objects.all() :
                if accion.id_uaysen.split("-")[0] == idPrefijo :
                    numeritos.append(int(accion.id_uaysen.split("-")[1]))
            numeritos.sort(reverse=True)
            if len(numeritos) > 0 :
                nuevoId = numeritos[0] + 1
            self.id_uaysen = "{}-{}".format(idPrefijo, nuevoId)
        super().save(*args, **kwargs)

class Proto_Rol(models.Model) :
    accion = models.ForeignKey('Proto_Accion', on_delete=models.CASCADE, verbose_name='Acción')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, blank=True, verbose_name='Depende de')
    tipo = models.CharField(max_length=MAX_LENGTH, verbose_name='Tipo de rol', choices=nombresRol)

class Proto_Hito(models.Model) :
    accion = models.ForeignKey('Proto_Accion', on_delete=models.CASCADE, verbose_name='Acción')
    nombre = models.TextField(verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción')
    plazo = models.ForeignKey('webapp.Plazo', on_delete=models.SET_NULL, null=True, verbose_name='Plazo')

    class Meta:
        verbose_name = PREFIJO_PROTO + "Hito"
        verbose_name_plural = PREFIJO_PROTO + "Hitos"

    def __str__(self):
        return '{}'.format(self.nombre)


class Proto_MDV(models.Model) :
    accion = models.ForeignKey('Proto_Accion', on_delete=models.CASCADE, verbose_name='Acción')
    nombre = models.TextField(verbose_name='Nombre')
    dirGoogle = models.CharField(max_length=MAX_LENGTH, verbose_name='ID en directorio en Google Drive', null=True)

    class Meta:
        verbose_name = PREFIJO_PROTO + "Medio de verificación"
        verbose_name_plural = PREFIJO_PROTO + "Medios de verificación"

    def __str__(self):
        return '{}'.format(self.nombre)


class Proto_CriterioMDV(models.Model) :
    criterio = models.TextField(verbose_name='Descripción del criterio')
    mdv = models.ForeignKey('Proto_MDV', on_delete=models.CASCADE, verbose_name='Medio de Verificación (MDV)')

    class Meta:
        verbose_name = PREFIJO_PROTO + "Criterio MDV"
        verbose_name_plural = PREFIJO_PROTO + "Criterios MDV"

    def __str__(self):
        return '{}'.format(self.criterio)


class Proto_Funcion(models.Model) :
    accion = models.ForeignKey('Proto_Accion', on_delete=models.CASCADE, verbose_name='Acción')
    nombre = models.TextField(verbose_name='Nombre de la función')
    dirGoogle = models.CharField(max_length=MAX_LENGTH, verbose_name='ID en directorio en Google Drive', null=True)
    
    class Meta:
        verbose_name = PREFIJO_PROTO + "Función"
        verbose_name_plural = PREFIJO_PROTO + "Funciones"

    def __str__(self):
        return '{}'.format(self.nombre)


class Proto_Indicador(models.Model) :
    funcion = models.ForeignKey('Proto_Funcion', on_delete=models.CASCADE, verbose_name='Función')
    nombre = models.TextField(verbose_name='Nombre del indicador')
    formula = models.TextField(verbose_name='Fórmula')
    meta = models.CharField(max_length=MAX_LENGTH, verbose_name='Meta', null=True)
    nombreVerificador = models.TextField(verbose_name='Verificador asociado', null=True)
    dirGoogle = models.CharField(max_length=MAX_LENGTH, verbose_name='ID en directorio en Google Drive', null=True)

    class Meta:
        verbose_name = PREFIJO_PROTO + "Indicador de función"
        verbose_name_plural = PREFIJO_PROTO + "Indicadores de una función"

    def __str__(self):
        return '{}'.format(self.nombre)


class Proto_Presupuesto(models.Model) :
    accion = models.ForeignKey('Proto_Accion', on_delete=models.CASCADE, verbose_name='Acción')
    ctaContable = models.ForeignKey('CtaContable', on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name='Descripción del gasto')
    total = models.IntegerField(verbose_name='Monto total (en miles)')

    class Meta:
        verbose_name = PREFIJO_PROTO + "Presupuesto"
        verbose_name_plural = PREFIJO_PROTO + "Presupuestos"

    def __str__(self):
        return '{}'.format(self.descripcion)


class Proto_Colaborador(models.Model) :
    accion = models.ForeignKey('Proto_Accion', on_delete=models.CASCADE, verbose_name='Acción')
    carrera = models.CharField(max_length=MIDDLE_LENGTH, choices=carreras, verbose_name="Carrera")
    semestre = models.PositiveSmallIntegerField(verbose_name="Semestre")
    asignatura = models.CharField(max_length=MAX_LENGTH, verbose_name="Asignatura")
    horas = models.PositiveIntegerField(verbose_name="Total horas de contrato")
    otrasHoras = models.PositiveIntegerField(verbose_name="Otras horas a contratar")
    valorHora = models.PositiveIntegerField(verbose_name="Valor hora (miles de pesos)")

    class Meta:
        verbose_name = PREFIJO_PROTO + "Colaborador"
        verbose_name_plural = PREFIJO_PROTO + "Colaboradores"

    def __str__(self):
        return '{} para {} para el semestre {}'.format(self.asignatura, self.carrera, self.horas)


class CtaContable(models.Model) :
    id_uaysen = models.CharField(max_length=MAX_LENGTH, verbose_name='Identificador interno')
    nombre = models.CharField(max_length=MAX_LENGTH, verbose_name='Nombre')
    item = models.CharField(max_length=MAX_LENGTH, verbose_name='Item')
    itemPresupuestario = models.CharField(max_length=MAX_LENGTH, verbose_name='Item presupuestario')

    class Meta:
        verbose_name = "Cuenta contable"
        verbose_name_plural = "Cuentas contables"

    def __str__(self):
        return '{} - {}'.format(self.id_uaysen, self.nombre)
