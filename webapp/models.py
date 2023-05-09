from django.db import models
from django.conf import settings
from django_fsm import FSMField, transition
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from simple_history.models import HistoricalRecords
import threading

MAX_LENGTH = 250
SHORT_LENGTH = 10
BYTES_LIMITE_CORREO_ELECTRICO = 25000000
PREFIJO_ASUNTO_MAIL = "[testing] "

deptos = [
    ('CSH', 'Ciencias Sociales y Humanidades'),
    ('CS', 'Ciencias de la Salud'),
    ('CNT', 'Ciencias Naturales y Tecnología')
]

tipoEstrategia = [
    ('PEDI', 'PEDI'),
    ('PDE', 'PDE'),
    ('PM', 'PM'),
]

tipoMeta = [
    (1, 'Entero'),
    (2, 'Porcentual'),
    (0, 'No definido'),
]

tiposCapacidad = [
    ('Estratégica', 'Estratégica'),
    ('Táctica', 'Táctica'),
    ('Táctica Estratégica', 'Táctica Estratégica'),
    ('Operativa', 'Operativa'),
    ('Docencia', 'Docencia'),
    ('Investigación', 'Investigación'),
    ('Vinculación con el Medio', 'Vinculación con el Medio'),
    ('Gestión Académica', 'Gestión Académica'),
    ('Soporte a la Gestión Académica', 'Soporte a la Gestión Académica'),
]

tiposAccion = [
    ('Misional', 'Misional'),
    ('Desarrollo', 'Desarrollo'),
]

tiposTactica = [
    ('Función', 'Función'),
    ('Hito', 'Hito')
]

coberturasTactica = [
    ('Acotada', 'Acotada'),
    ('Mediana', 'Mediana'),
    ('Mínima', 'Mínima'),
    ('Amplia', 'Amplia'),
]

naturalezasTactica = [
    ('Analítica', 'Analítica'),
    ('Técnica', 'Técnica'),
]

prioridadTactica = [
    ('Alta', 'Alta'),
    ('Normal', 'Normal'),
    ('Baja', 'Baja'),
]

nombresRol = [
    ('Aprobador', 'Aprobador'),
    ('Consultado', 'Consultado'),
    ('Informado', 'Informado'),
    ('Responsable', 'Responsable'),
    ('Soporte', 'Soporte'),
]

tiposParticipacionRol = [
    ('Normal', 'Normal'),
    ('Esporádica', 'Esporádica'),
    ('Puntual', 'Puntual'),
]

meses = [
    ('ene', 'Enero'),
    ('feb', 'Febrero'),
    ('mar', 'Marzo'),
    ('abr', 'Abril'),
    ('may', 'Mayo'),
    ('jun', 'Junio'),
    ('jul', 'Julio'),
    ('ago', 'Agosto'),
    ('sep', 'Septiembre'),
    ('oct', 'Octubre'),
    ('nov', 'Noviembre'),
    ('dic', 'Diciembre'),
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
]

tipoCategorias = [
    ('académicas', 'académicas'),       # GA (de "gestión académica")
    ('operativos', 'operativos'),       # OP
    ('tácticos', 'tácticos'),           # TAC
    ('colegiado', 'colegiado'),         # COL
    ('estratégicas', 'estratégicas')    # ESTR
                                        # y TODOS para todos
]

indicadorLogro = [
    ('Logrado', 'Logrado'),
    ('Logrado con atrasos', 'Logrado con atrasos'),
    ('No logrado', 'No logrado')
]

class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html, adjunto):
        self.subject = PREFIJO_ASUNTO_MAIL + subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        self.adjunto = adjunto
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        if self.adjunto and self.adjunto.size < BYTES_LIMITE_CORREO_ELECTRICO:
            msg.attach_file(self.adjunto.file.name)
        msg.send(self.fail_silently)

def async_send_mail(subject, body, from_email, recipient_list, fail_silently=False, html=None, adjunto=None, *args, **kwargs):
    # Robert: Descomentar la siguiente linea para activar el spam :-D
    # EmailThread(subject, body, from_email, recipient_list, fail_silently, html, adjunto).start()
    EmailThread(subject, body, from_email, ['sebastian.saez@uaysen.cl'], fail_silently, html, adjunto).start()

class Plazo(models.Model) :
    '''
    Representa una fecha limite de entrega
    '''
    plazo_anio = models.PositiveIntegerField(choices=anios, verbose_name='Año', help_text='Número que representa el año de la fecha plazo a la que se debe entregar el elemento asociado')
    plazo_mes = models.CharField(max_length=MAX_LENGTH, choices=meses, verbose_name='Mes', help_text='Nombre del mes de la fecha plazo a la que se debe entregar el elemento asociado')

    class Meta:
        verbose_name = "Plazo"
        verbose_name_plural = "Plazos"

    def __str__(self):
        return '{} del {}'.format(self.plazo_mes, self.plazo_anio)

class Periodo(models.Model) :
    '''
    Representa un rango de validez delimitado por un año de inicio y término
    '''
    anio_inicio = models.PositiveIntegerField(choices=anios, verbose_name='Año', help_text='Año inicio del periodo')
    anio_fin = models.PositiveIntegerField(choices=anios, verbose_name='Año', help_text='Año fin del periodo')

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"

    def __str__(self):
        return 'de {} a {}'.format(self.anio_inicio, self.anio_fin)

class Estrategia(models.Model) :
    '''
    Representa a las estrategias de la universidad definidas por PEDI, Plan de mejoras y Planes de deptos
    '''
    id_uaysen = models.CharField(max_length=MAX_LENGTH, verbose_name='Identificador interno')
    ambito = models.CharField(max_length=MAX_LENGTH, verbose_name='Ámbito')
    tipo = models.CharField(max_length=SHORT_LENGTH, verbose_name='Tipo', choices=tipoEstrategia)
    descripcion = models.TextField(verbose_name='Descripción')
    periodo = models.ForeignKey('Periodo', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Periodo de actividad')

    class Meta:
        verbose_name = "Estrategia"
        verbose_name_plural = "Estrategias"

    def __str__(self):
        return '{}'.format(self.id_uaysen)

class Accion(models.Model) :
    estrategias = models.ManyToManyField('Estrategia')
    dimensiones = models.ManyToManyField('Dimension')
    id_uaysen = models.CharField(max_length=MAX_LENGTH, verbose_name='Identificador interno')
    proyecto = models.CharField(max_length=MAX_LENGTH, null=True, verbose_name='Proyecto URY')
    anio = models.PositiveIntegerField(choices=anios, verbose_name='Año')
    titulo = models.TextField(verbose_name='Título')
    objetivo = models.TextField(verbose_name='Objetivo')
    tipo = models.CharField(max_length=MAX_LENGTH, choices=tiposAccion, verbose_name='Tipo de acción')
    presupuesto = models.PositiveIntegerField(verbose_name='Presupuesto en pesos chilenos', null=True)
    origen = models.CharField(max_length=MAX_LENGTH, verbose_name='Orígen de la acción', default='POA')
    dirGoogle = models.CharField(max_length=MAX_LENGTH, null=True, verbose_name='ID en directorio en Google Drive')

    class Meta:
        verbose_name = "Acción"
        verbose_name_plural = "Acciones"

    def __str__(self):
        return '{}: {}'.format(self.id_uaysen, self.titulo)

class Dimension(models.Model) :
    nombre = models.CharField(max_length=MAX_LENGTH, verbose_name='Nombre Dimensión')
    texto_ley = models.CharField(max_length=MAX_LENGTH, verbose_name='Texto Ley', null=True, blank=True)
    class Meta:
        verbose_name = "Dimensión CNA"
        verbose_name_plural = "Dimensiones CNA"

    def __str__(self):
        return '{} ({})'.format(self.nombre, self.texto_ley)

class Reporte (models.Model) :
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actor = models.ForeignKey('Actor', on_delete=models.CASCADE, null=True)
    modificado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, verbose_name='Estado reporte')
    recomendacion = models.TextField(verbose_name='Recomendación a la unidad', null=True, blank=True)
    tipo = models.CharField(max_length=SHORT_LENGTH, verbose_name='Tipo de Reporte', default='POA')
    enviado = models.BooleanField(default=False, verbose_name='Indica si reporte ha sido enviado al Actor')

    class Meta:
        verbose_name = "Reporte de la unidad"
        verbose_name_plural = "Reportes de la unidad"

    def __str__(self):
        txt = "Recomendación"
        txt+= " de {}: {}".format("actor", self.recomendacion)
        return txt

class ReporteAccion (models.Model) :
    accion = models.ForeignKey('Accion',on_delete=models.CASCADE, verbose_name='Acción')
    detalle_reporte = models.ForeignKey(Reporte,on_delete=models.CASCADE, related_name='reporte_acciones')
    estado_ejecucion = models.TextField(verbose_name='Estado ejecución de la acción', null=True, blank=True)
    justificacion_contingencia = models.CharField('Justificación por contingencia',max_length=MAX_LENGTH, null=True, blank=True)
    reporte_justificacion_contingencia = models.TextField(verbose_name='Documento Justificación por contingencia', null=True, blank=True)
    indicador = models.TextField('Indicador Reporte PMI', null=True)
    indicador_logro = models.CharField('Indicador Logro Reporte PMI',max_length=MAX_LENGTH, null=True, blank=True)

    class Meta:
        verbose_name = "Reporte accion"
        verbose_name_plural = "Reportes acciones"

class ReporteFuncion (models.Model) :
    dependencia = models.ForeignKey(ReporteAccion,related_name='reporte_funciones',on_delete=models.CASCADE, null=True)
    id_tactica = models.CharField('Id Tactica', max_length=MAX_LENGTH, null=True)
    funcion = models.ForeignKey('Funcion', on_delete=models.SET_NULL, null=True)
    indicador = models.PositiveIntegerField('Indicador', null=True)
    comentario_cumplimiento = models.TextField(verbose_name='Comentarios de cumplimiento', null=True, blank=True)

    class Meta:
        verbose_name = "Reporte funcion"
        verbose_name_plural = "Reportes funciones"

class ReporteHito (models.Model) :
    dependencia = models.ForeignKey(ReporteAccion,related_name='reporte_hitos',on_delete=models.CASCADE, null=True)
    id_tactica = models.CharField('Id Tactica', max_length=MAX_LENGTH, null=True)
    mdvs = models.ManyToManyField('MDV', related_name='mdvs', blank=True, null=True)
    hito = models.ForeignKey('Hito',on_delete=models.SET_NULL, null=True,related_name='hitos')
    indicador = models.PositiveIntegerField('Indicador', null=True)
    indicador_logro = models.CharField('Indicador Logro',max_length=MAX_LENGTH, null=True, blank=True)
    justificacion_contingencia = models.CharField('Justificación por contingencia PMI',max_length=MAX_LENGTH, null=True, blank=True)
    reporte_justificacion_contingencia = models.TextField(verbose_name='Documento Justificación por contingencia PMI', null=True, blank=True)
    comentario_cumplimiento = models.TextField(verbose_name='Comentarios de cumplimiento', null=True, blank=True)

    class Meta:
        verbose_name = "Reporte hitos"
        verbose_name_plural = "Reportes hitos"

class Actor(models.Model) :
    nombre = models.CharField(max_length=MAX_LENGTH, verbose_name='Nombre')
    id_uaysen = models.CharField(max_length=MAX_LENGTH, verbose_name='Identificador interno')
    sigla = models.CharField(max_length=SHORT_LENGTH, verbose_name='Sigla')
    cai = models.CharField(max_length=SHORT_LENGTH, verbose_name='CAI')
    es_area = models.BooleanField(default=False, verbose_name='Indica si actor es área estratégica')
    categoria = models.CharField(max_length=MAX_LENGTH, verbose_name='Categoria de unidad', null=True, choices=tipoCategorias)
    dependencia = models.ForeignKey('Actor', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Dependencia del actor')
    es_direccion = models.BooleanField(default=False, verbose_name='Indica si actor es dirección')
    
    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actores"

    def __str__(self):
        return '{} ({})'.format(self.nombre, self.sigla)

class Funcion(models.Model) :
    accion = models.ForeignKey('Accion', on_delete=models.CASCADE, verbose_name='Acción')
    nombre = models.TextField(verbose_name='Nombre de la función')
    dirGoogle = models.CharField(max_length=MAX_LENGTH, verbose_name='ID en directorio en Google Drive', null=True)
    
    class Meta:
        verbose_name = "Función"
        verbose_name_plural = "Funciones"

    def __str__(self):
        return '{}'.format(self.nombre)

class Indicador(models.Model) :
    funcion = models.ForeignKey('Funcion', on_delete=models.CASCADE, verbose_name='Función')
    nombre = models.TextField(verbose_name='Nombre del indicador')
    formula = models.TextField(verbose_name='Fórmula')
    meta = models.CharField(max_length=MAX_LENGTH, verbose_name='Meta', null=True)
    tipo_indicador = models.CharField(max_length=SHORT_LENGTH, verbose_name='Tipo Indicador', choices=tipoMeta, default = 0)
    nombreVerificador = models.TextField(verbose_name='Verificador asociado', null=True)
    dirGoogle = models.CharField(max_length=MAX_LENGTH, verbose_name='ID en directorio en Google Drive', null=True)

    class Meta:
        verbose_name = "Indicador de función"
        verbose_name_plural = "Indicadores de una función"

    def __str__(self):
        return '{}'.format(self.nombre)

class Verificador(models.Model) :
    '''
    Entrega de una función
    '''
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    indicador = models.ForeignKey('Indicador', on_delete=models.CASCADE, null=True)
    valor = models.CharField(max_length=MAX_LENGTH, verbose_name="Valor", help_text="Valor calculado según la fórmula de la entrega del indicador de la función")
    descripcion = models.TextField(verbose_name='Descripción del valor')
    adjuntos = models.JSONField(null=True)
    estado = FSMField(default='Borrador')
    modificado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)
    #history = HistoricalRecords()

    def __str__(self):
        return '{} de {}'.format(self.descripcion, self.usuario.email if self.usuario else '<usuario eliminado>')

    @transition(field=estado, source='Borrador', target='Enviado al líder')
    @transition(field=estado, source='Rechazado por líder', target='Enviado al líder')
    def envia_a_lider(self):
        contexto = {
            "nombre_usuario" : self.usuario.first_name,
            "tipo_entrega" : "verificador",
            "id_accion" : self.indicador.funcion.accion.id_uaysen
        }
        # envío de correo al colaborador que subió la entrega
        html_content = loader.render_to_string("webapp/correo_EnviaAlLider_colaborador.html", contexto)
        subject = "Entrega " + str(self.id) + " enviada a encargados responsables de la acción"
        body = "Entrega " + str(self.id) + " enviada"
        from_email = "colabora@uaysen.cl"
        recipient_list = [self.usuario.email]
        async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)
        # envío de correo a los encargados de unidad responsables de la acción
        for usuario in User.objects.filter(
            perfilusuario__actor__rol__tipo='Responsable',
            perfilusuario__es_encargado=True,
            perfilusuario__actor__rol__accion=self.indicador.funcion.accion).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "tipo_entrega" : "verificador",
                "id_accion" : self.indicador.funcion.accion.id_uaysen
            }        
            html_content = loader.render_to_string("webapp/correo_EnviaAlLider_encargado.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a encargados responsables de la acción"
            body = "Entrega " + str(self.id) + " enviada"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)

    @transition(field=estado, source='Enviado al líder', target='Rechazado por líder')
    def rechaza_lider(self, retro=''):
        contexto = {
            "nombre_usuario" : self.usuario.first_name,
            "tipo_entrega" : "verificador",
            "retroalimentacion" : retro
        }
        # envío de correo al lider que rechazó
        html_content = loader.render_to_string("webapp/correo_RechazadoPorLider_colaborador.html", contexto)
        subject = "Entrega " + str(self.id) + " enviada al colaborador de la entrega rechazada"
        body = "Entrega " + str(self.id) + " rechazada"
        from_email = "colabora@uaysen.cl"
        recipient_list = [self.usuario.email]
        async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)

        # envío de correo a los encargados de unidad responsables de la acción
        for usuario in User.objects.filter(
            perfilusuario__actor__rol__tipo='Responsable',
            perfilusuario__es_encargado=True,
            perfilusuario__actor__rol__accion=self.indicador.funcion.accion).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "tipo_entrega" : "verificador",
                "id_accion" : self.indicador.funcion.accion.id_uaysen,
                "retroalimentacion" : retro
            }        
            html_content = loader.render_to_string("webapp/correo_RechazadoPorLider_encargado.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a todos los encargados responsables de la acción"
            body = "Entrega " + str(self.id) + " rechazada"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)

    @transition(field=estado, source='Enviado al líder', target='Enviado a UPCI')
    @transition(field=estado, source='Rechazado por UPCI', target='Enviado a UPCI')
    def envia_a_UPCI(self):
        contexto = {
            "nombre_usuario" : self.usuario.first_name,
            "tipo_entrega" : "verificador",
        }
        # envío de correo al colaborador
        html_content = loader.render_to_string("webapp/correo_EnviaAUPCI_colaborador.html", contexto)
        subject = "Entrega " + str(self.id) + " enviada a equipo UPCI"
        body = "Entrega " + str(self.id) + " enviada"
        from_email = "colabora@uaysen.cl"
        recipient_list = [self.usuario.email]
        async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)
        # envío de correo al equipo UPCI
        for usuario in User.objects.filter(perfilusuario__es_analistaUPCI=True).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "tipo_entrega" : "verificador",
                "id_accion" : self.indicador.funcion.accion.id_uaysen
            }        
            html_content = loader.render_to_string("webapp/correo_EnviaAUPCI_upci.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a todos los analistas UPCI"
            body = "Entrega " + str(self.id) + " comunicada al equipo UPCI"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)

    @transition(field=estado, source='Enviado a UPCI', target='Finalizado')
    def acepta_UPCI(self):
        contexto = {
            "nombre_usuario" : self.usuario.first_name,
            "tipo_entrega" : "verificador",
        }
        # envío de correo al colaborador que subió la entrega
        html_content = loader.render_to_string("webapp/correo_Finalizado_colaborador.html", contexto)
        subject = "Entrega " + str(self.id) + " enviada al colaborador"
        body = "Entrega " + str(self.id) + " finalizada"
        from_email = "colabora@uaysen.cl"
        recipient_list = [self.usuario.email]
        async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)
        # envío de correo a los encargados de unidad responsables de la acción
        for usuario in User.objects.filter(
            perfilusuario__actor__rol__tipo='Responsable',
            perfilusuario__es_encargado=True,
            perfilusuario__actor__rol__accion=self.indicador.funcion.accion).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "tipo_entrega" : "verificador",
                "id_accion" : self.indicador.funcion.accion.id_uaysen
            }        
            html_content = loader.render_to_string("webapp/correo_Finalizado_encargado.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a todos los encargados responsables de la acción"
            body = "Entrega " + str(self.id) + " finalizada"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)
        # envío de correo al equipo UPCI
        for usuario in User.objects.filter(perfilusuario__es_analistaUPCI=True).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "tipo_entrega" : "verificador",
                "id_accion" : self.indicador.funcion.accion.id_uaysen
            }        
            html_content = loader.render_to_string("webapp/correo_Finalizado_upci.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a todos los analistas UPCI"
            body = "Entrega " + str(self.id) + " finalizada"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)

    @transition(field=estado, source='Enviado a UPCI', target='Rechazado por UPCI')
    def rechazado_UPCI(self, retro=''):
        contexto = {
            "nombre_usuario" : self.usuario.first_name,
            "tipo_entrega" : "verificador",
            "retroalimentacion" : retro
        }
        # envío de correo al colaborador que subió la entrega
        html_content = loader.render_to_string("webapp/correo_RechazadoPorUPCI_colaborador.html", contexto)
        subject = "Entrega " + str(self.id) + " enviada a encargados responsables de la acción"
        body = "Entrega " + str(self.id) + " enviada"
        from_email = "colabora@uaysen.cl"
        recipient_list = [self.usuario.email]
        async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)
        # envío de correo a los encargados de unidad responsables de la acción
        for usuario in User.objects.filter(perfilusuario__actor__rol__tipo='Responsable', perfilusuario__es_encargado=True).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "tipo_entrega" : "verificador",
                "id_accion" : self.indicador.funcion.accion.id_uaysen,
                "retroalimentacion" : retro
            }        
            html_content = loader.render_to_string("webapp/correo_RechazadoPorUPCI_encargado.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a todos los encargados responsables de la acción"
            body = "Entrega " + str(self.id) + " rechazada"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)

    class Meta:
        verbose_name = "Verificador"
        verbose_name_plural = "Verificadores"

class Hito(models.Model) :
    accion = models.ForeignKey('Accion', on_delete=models.CASCADE, verbose_name='Acción')
    nombre = models.TextField(verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción')
    plazo = models.ForeignKey('Plazo', on_delete=models.SET_NULL, null=True, verbose_name='Plazo')
    dirGoogle = models.CharField(max_length=MAX_LENGTH, verbose_name='ID en directorio en Google Drive', null=True)

    class Meta:
        verbose_name = "Hito"
        verbose_name_plural = "Hitos"

    def __str__(self):
        return '{}'.format(self.nombre)

class MDV(models.Model) :
    '''
    MDV = Medio de verificación. Se asocian a los hitos
    Se acordó de llamar PRODUCTO a las entregas de MDVs, los que deben
    cumplir ciertos criterios (definidos más abajo)
    '''
    accion = models.ForeignKey('Accion', on_delete=models.CASCADE, verbose_name='Acción')
    nombre = models.TextField(verbose_name='Nombre')
    dirGoogle = models.CharField(max_length=MAX_LENGTH, verbose_name='ID en directorio en Google Drive', null=True)

    class Meta:
        verbose_name = "Medio de verificación"
        verbose_name_plural = "Medios de verificación"

    def __str__(self):
        return '{}'.format(self.nombre)

class CriterioMDV(models.Model) :
    criterio = models.TextField(verbose_name='Descripción del criterio')
    mdv = models.ForeignKey('MDV', on_delete=models.CASCADE, verbose_name='Medio de Verificación (MDV)')

    def __str__(self):
        return '{}'.format(self.criterio)

class Producto(models.Model) :
    '''
    Entrega de un MDV (hito + criterios) de una acción
    '''
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    mdv = models.ForeignKey('MDV', on_delete=models.CASCADE,blank=True, null=True)
    hitos = models.ManyToManyField('Hito')
    descripcion = models.TextField(verbose_name='Descripción del producto entregado')
    adjuntos = models.JSONField(null=True)
    estado = FSMField(default='Borrador')
    modificado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)
    #history = HistoricalRecords()

    def __str__(self):
        return '{} de {}'.format(self.descripcion, self.usuario.email if self.usuario else '<usuario eliminado>')

    @transition(field=estado, source='Borrador', target='Enviado al líder')
    @transition(field=estado, source='Rechazado por líder', target='Enviado al líder')
    def envia_a_lider(self):
        if self.mdv:            
            id_accion = self.mdv.accion
        else:
            id_accion = self.hitos.first().accion

        contexto = {
            "nombre_usuario" : self.usuario.first_name,
            "tipo_entrega" : "producto",
            "id_accion" : id_accion.id_uaysen
        }
        # envío de correo al colaborador que subió la entrega
        html_content = loader.render_to_string("webapp/correo_EnviaAlLider_colaborador.html", contexto)
        subject = "Entrega " + str(self.id) + " enviada a encargados responsables de la acción"
        body = "Entrega " + str(self.id) + " enviada"
        from_email = "colabora@uaysen.cl"
        recipient_list = [self.usuario.email]
        async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)
        # envío de correo a los encargados de unidad responsables de la acción
        for usuario in User.objects.filter(
            perfilusuario__actor__rol__tipo='Responsable',
            perfilusuario__es_encargado=True,
            #perfilusuario__actor__rol__accion=self.mdv.accion).distinct() :
            perfilusuario__actor__rol__accion=id_accion.id).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "nombre_colaborador" : self.usuario.first_name,
                "tipo_entrega" : "producto",
            #    "id_accion" : self.mdv.accion.id_uaysen
                "id_accion" : id_accion.id_uaysen
            }        
            html_content = loader.render_to_string("webapp/correo_EnviaAlLider_encargado.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a líderes"
            body = "Entrega " + str(self.id) + " enviada"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)

    @transition(field=estado, source='Enviado al líder', target='Rechazado por líder')
    def rechaza_lider(self, retro=''):
        if self.mdv:            
            id_accion = self.mdv.accion
        else:
            id_accion = self.hitos.first().accion

        contexto = {
            "nombre_usuario" : self.usuario.first_name,
            "tipo_entrega" : "producto",
            "retroalimentacion" : retro
        }
        # envío de correo al lider que rechazó
        html_content = loader.render_to_string("webapp/correo_RechazadoPorLider_colaborador.html", contexto)
        subject = "Entrega " + str(self.id) + " enviada al colaborador de la entrega rechazada"
        body = "Entrega " + str(self.id) + " rechazada"
        from_email = "colabora@uaysen.cl"
        recipient_list = [self.usuario.email]
        async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)
        # envío de correo a los encargados de unidad responsables de la acción
        for usuario in User.objects.filter(
            perfilusuario__actor__rol__tipo='Responsable',
            perfilusuario__es_encargado=True,
            #perfilusuario__actor__rol__accion=self.mdv.accion).distinct() :
            perfilusuario__actor__rol__accion=id_accion.id).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "tipo_entrega" : "producto",
                #"id_accion" : self.mdv.accion.id_uaysen,
                "id_accion" : id_accion.id_uaysen,
                "retroalimentacion" : retro
            }        
            html_content = loader.render_to_string("webapp/correo_RechazadoPorLider_encargado.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a todos los encargados responsables de la acción"
            body = "Entrega " + str(self.id) + " rechazada"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)

    @transition(field=estado, source='Enviado al líder', target='Enviado a UPCI')
    @transition(field=estado, source='Rechazado por UPCI', target='Enviado a UPCI')
    def envia_a_UPCI(self):
        if self.mdv:            
            id_accion = self.mdv.accion
        else:
            id_accion = self.hitos.first().accion

        contexto = {
            "nombre_usuario" : self.usuario.first_name,
            "tipo_entrega" : "producto",
        }
        # envío de correo al colaborador
        html_content = loader.render_to_string("webapp/correo_EnviaAUPCI_colaborador.html", contexto)
        subject = "Entrega " + str(self.id) + " enviada a equipo UPCI"
        body = "Entrega " + str(self.id) + " enviada"
        from_email = "colabora@uaysen.cl"
        recipient_list = [self.usuario.email]
        async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)
        # envío de correo al equipo UPCI
        for usuario in User.objects.filter(perfilusuario__es_analistaUPCI=True).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "tipo_entrega" : "producto",
                #"id_accion" : self.mdv.accion.id_uaysen
                "id_accion"  : id_accion.id_uaysen
            }        
            html_content = loader.render_to_string("webapp/correo_EnviaAUPCI_upci.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a todos los analistas UPCI"
            body = "Entrega " + str(self.id) + " comunicada al equipo UPCI"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)

    @transition(field=estado, source='Enviado a UPCI', target='Finalizado')
    def acepta_UPCI(self):
        if self.mdv:            
            id_accion = self.mdv.accion
        else:
            id_accion = self.hitos.first().accion

        contexto = {
            "nombre_usuario" : self.usuario.first_name,
            "tipo_entrega" : "producto",
        }
        # envío de correo al colaborador que subió la entrega
        html_content = loader.render_to_string("webapp/correo_Finalizado_colaborador.html", contexto)
        subject = "Entrega " + str(self.id) + " enviada al colaborador"
        body = "Entrega " + str(self.id) + " finalizada"
        from_email = "colabora@uaysen.cl"
        recipient_list = [self.usuario.email]
        async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)
        # envío de correo a los encargados de unidad responsables de la acción
        for usuario in User.objects.filter(
            perfilusuario__actor__rol__tipo='Responsable',
            perfilusuario__es_encargado=True,
            perfilusuario__actor__rol__accion=id_accion.id).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "tipo_entrega" : "producto",
                #"id_accion" : self.mdv.accion.id_uaysen
                "id_accion"  : id_accion.id_uaysen
            }        
            html_content = loader.render_to_string("webapp/correo_Finalizado_encargado.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a todos los encargados responsables de la acción"
            body = "Entrega " + str(self.id) + " finalizada"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)
        # envío de correo al equipo UPCI
        for usuario in User.objects.filter(perfilusuario__es_analistaUPCI=True).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "tipo_entrega" : "producto",
                #"id_accion" : self.mdv.accion.id_uaysen
                "id_accion"  : id_accion.id_uaysen
            }        
            html_content = loader.render_to_string("webapp/correo_Finalizado_upci.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a todos los analistas UPCI"
            body = "Entrega " + str(self.id) + " finalizada"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)

    @transition(field=estado, source='Enviado a UPCI', target='Rechazado por UPCI')
    def rechazado_UPCI(self, retro=''):
        if self.mdv:            
            id_accion = self.mdv.accion
        else:
            id_accion = self.hitos.first().accion

        contexto = {
            "nombre_usuario" : self.usuario.first_name,
            "tipo_entrega" : "producto",
            "retroalimentacion" : retro
        }
        # envío de correo al colaborador que subió la entrega
        html_content = loader.render_to_string("webapp/correo_RechazadoPorUPCI_colaborador.html", contexto)
        subject = "Entrega " + str(self.id) + " enviada a encargados responsables de la acción"
        body = "Entrega " + str(self.id) + " enviada"
        from_email = "colabora@uaysen.cl"
        recipient_list = [self.usuario.email]
        async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)
        # envío de correo a los encargados de unidad responsables de la acción
        for usuario in User.objects.filter(perfilusuario__actor__rol__tipo='Responsable', perfilusuario__es_encargado=True).distinct() :
            contexto = {
                "nombre_usuario" : usuario.first_name,
                "tipo_entrega" : "producto",
                #"id_accion" : self.mdv.accion.id_uaysen,
                "id_accion"  : id_accion.id_uaysen,
                "retroalimentacion" : retro
            }        
            html_content = loader.render_to_string("webapp/correo_RechazadoPorUPCI_encargado.html", contexto)
            subject = "Entrega " + str(self.id) + " enviada a todos los encargados responsables de la acción"
            body = "Entrega " + str(self.id) + " rechazada"
            from_email = "colabora@uaysen.cl"
            recipient_list = [usuario.email]
            async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=None)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class RetroEntrega(models.Model) :
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, null=True)
    verificador = models.ForeignKey('Verificador', on_delete=models.CASCADE, null=True)
    retroalimentacion = models.TextField(verbose_name='Retralimentación de la entrega')
    modificado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Retroalimentación de entrega"
        verbose_name_plural = "Retroalimentaciones de entregas"

    def __str__(self):
        txt = "Retroalimentación"
        if self.producto :
            txt += " de {}: {}".format("producto", self.retroalimentacion)
        elif self.verificador :
            txt += " de {}: {}".format("verificador", self.retroalimentacion)
        return txt

class Rol(models.Model) :
    accion = models.ForeignKey('Accion', on_delete=models.CASCADE, verbose_name='Acción')
    actor = models.ForeignKey('Actor', on_delete=models.CASCADE, blank=True, verbose_name='Depende de')
    tipo = models.CharField(max_length=MAX_LENGTH, verbose_name='Tipo de rol', choices=nombresRol)

    class Meta:
        verbose_name = "Rol de un actor en una acción"
        verbose_name_plural = "Roles de actores en acciones"

    def __str__(self):
        return '{} en {}'.format(self.actor.nombre, self.accion.id_uaysen)

class PerfilUsuario(models.Model) :
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actor = models.ForeignKey('Actor', on_delete=models.SET_NULL, null=True)
    es_encargado = models.BooleanField(default=False)
    es_analistaUPCI = models.BooleanField(default=False)
    foto = models.URLField(max_length=MAX_LENGTH)
    sesion = models.JSONField()

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de los usuarios"

    def __str__(self):
        if self.actor :
            return 'Perfil de {} miembro de {}'.format(self.usuario.username, self.actor.nombre)
        else :
            return 'Perfil de {}'.format(self.usuario.username)

class Meta(models.Model) :
    matrizAccionEstrategia = models.JSONField()
