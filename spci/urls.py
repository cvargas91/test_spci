"""spci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from webapp import views
from creadorpoas import views as views_creadorpoas
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'accion', views.AccionViewSet)
router.register(r'verificador', views.VerificadorViewSet)
router.register(r'_verificador', views.VerificadorDepthViewSet)
router.register(r'producto', views.ProductoViewSet)
router.register(r'_producto', views.ProductoDepthViewSet)
router.register(r'retroEntrega', views.RetroEntregaViewSet)
router.register(r'roles', views.RolViewSet)
router.register(r'mdv', views.MDVViewSet)
router.register(r'hito', views.HitoViewSet)
router.register(r'indicador', views.IndicadorViewSet)
router.register(r'funcion', views.FuncionViewSet)
router.register(r'editaVerificador', views.EditaVerificadorViewSet)
router.register(r'editaProducto', views.EditaProductoViewSet)
router.register(r'estrategia', views.EstrategiaViewSet)
# endpoints creador poas
router.register(r'protoAccion', views_creadorpoas.Proto_Accion_ViewSet)
router.register(r'_protoAccion', views_creadorpoas.Proto_Accion_Depth_ViewSet)
router.register(r'protoHito', views_creadorpoas.Proto_Hito_ViewSet)
router.register(r'protoMDV', views_creadorpoas.Proto_MDV_ViewSet)
router.register(r'protoCriterioMDV', views_creadorpoas.Proto_CriterioMDV_ViewSet)
router.register(r'protoFuncion', views_creadorpoas.Proto_Funcion_ViewSet)
router.register(r'protoIndicador', views_creadorpoas.Proto_Indicador_ViewSet)
router.register(r'protoPresupuesto', views_creadorpoas.Proto_Presupuesto_ViewSet)
router.register(r'protoColaborador', views_creadorpoas.Proto_Colaborador_ViewSet)
router.register(r'ctaContable', views_creadorpoas.CtaContable_ViewSet)
# FIN endpoints creador poas
router.register(r'actor', views.ActorViewSet)
router.register(r'reporte', views.ReportesViewSet)

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('', views.index, name='index'),
    path('seteaPerfil/', views.seteaPerfil, name='seteaPerfil'),
    path('gCallback/', views.gCallback, name='gCallback'),
    path('gRedirect/', views.gRedirect, name='gRedirect'),
    path('getCredentials/', views.getCredentials, name='getCredentials'),
    path('datosIniciales/', login_required(views.datosIniciales), name='datosIniciales'),
    ####### Backend flujo de estados del entregable
    path('entregableEnviaALider/', views.entregableEnviaALider, name='entregableEnviaALider'),
    path('entregableLiderDaVistoBueno/', views.entregableLiderDaVistoBueno, name='entregableLiderDaVistoBueno'),
    path('entregableUPCIDaVistoBueno/', views.entregableUPCIDaVistoBueno, name='entregableUPCIDaVistoBueno'),
    path('entregableLiderRechaza/', views.entregableLiderRechaza, name='entregableLiderRechaza'),
    path('entregableUPCIRechaza/', views.entregableUPCIRechaza, name='entregableUPCIRechaza'),
    path('entregableDescarta/', views.entregableDescarta, name='entregableDescarta'),

    path('generarPdf/<int:id_reporte>', views.ReporteUpciPDFViewSet.as_view(), name='generarReporteUpci'),
    #path('generarPdfTest/', views.ReporteUpciPDFViewSet4.as_view(), name='generarReporteUpci'),
    path('generarPdfPMI/<int:id_reporte>', views.ReporteUpciPmiPDFViewSet.as_view(), name='generarReporteUpciPMI'),
    #path('generarPdfTestPMI/', views.ReporteUpciPmiPDFViewSet4.as_view(), name='generarReporteUpci'),
    
    path('accionesFiltradas/', views.accionesFiltradas, name='accionesFiltradas'),
    path('app/', login_required(views.app), name='app'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    # solo como testing:
    path('404/', views.permission_denied_view, name='permission_denied_view'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler403 = 'webapp.views.cuatrocientoscuatro'