from django.urls import path, register_converter
from django.conf import settings
from django.conf.urls.static import static

from datetime import date, datetime, timedelta
from . import views
from django.urls import path 
from .views import deudas_list 
from .views import generate_pdf
#from django.views.generic import RedirectView

# Template urls
app_name = 'condominio_app'

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy')

urlpatterns = [
    
   
    #reporte de deudas
    
    path('recibo_total_deuda/<int:id>', views.recibo_total_deuda, name='r ecibo_total_deuda'),
    path('deudas_list/', views.deudas_list, name='deudas_list'),
    # Vistas de usuario
    path('', views.home, name='home'),
    #path('', RedirectView.as_view(url='home/', permanent=False)),
    path('check-static/', views.check_static, name='check_static'),
    path('check-settings/', views.check_settings, name='check_settings'),
    path('check-database/', views.check_database, name='check_database'),
    path('alquileres/', views.alquileresRedic, name='alquileres'),
    path('conf_reserva/', views.conf_reserva, name='conf_reserva'),
    path('update_view/<id_reservacion>', views.update_view, name='update_view'),
    path('editarEstado/', views.editarEstado, name='editarEstado'),
    path('domicilio_update/', views.domicilio_update, name='domicilio_update'),
    path('viviendas/', views.viviendas, name='viviendas'),
    path('local-comercial/', views.local_comercial, name='local_comercial'),
    path('alquiler-residencial/', views.alquiler_residencial, name='alquiler_residencial'),
    path('alquiler-vacacional/', views.alquiler_vacacional, name='alquiler_vacacional'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('cartelera-informativa/', views.cartelera_informativa, name='cartelera_informativa'),
    path('contacto/', views.contacto, name='contacto'),
    path('contacto/send_mail/', views.send_mail, name='send_mail'),
    path('cartelera-informativa/<slug>/', views.noticia, name="noticia"),
    path('reservacion/', views.reservacion, name="reservacion"),

    # Vistas de propietario
    path('home/propietarios/', views.home_propietarios, name='home_propietarios'),
    path('home/propietarios/pagos/', views.propietarios_pagos, name='propietarios_pagos'),
    path('home/propietarios/publicaciones/', views.propietarios_publicaciones, name='propietarios_publicaciones'),
    path('home/propietarios/recibos/', views.propietarios_recibos, name='propietarios_recibos'),
    path('home/propietarios/recibos/pdf/<int:id>', views.propietario_recibo_pago, name='propietario_recibo_pago'),

    # Vistas de administrador
    
    path('home/administrador/añadir_alquiler', views.añadir_alquiler, name='añadir_alquiler'),
    path('home/administrador/', views.home_admin, name='home_admin'),
    path('home/administrador/perfil/', views.admin_perfil, name="admin_perfil"),
    path('home/administrar/bancos/', views.admin_bancos, name="admin_bancos"),
    path('home/administrar/gastos/', views.admin_gastos, name="admin_gastos"),
    path('home/administrar/ingresos/', views.admin_ingresos, name="admin_ingresos"),
    path('home/administrar/deudas/', views.admin_deudas, name="admin_deudas"),
    path('home/administrar/deudas/abonar/<int:id>', views.admin_abono_deudas, name="admin_abono_deudas"),
    path('home/administrar/fondos/', views.admin_fondos, name="admin_fondos"),
    path('home/administrar/propietarios/', views.admin_propietarios, name="admin_propietarios"),
    path('home/administrar/propietarios/movimiento/', views.admin_propietarios_mov, name="admin_propietarios_mov"),
    path('home/administrar/validacion-pagos/', views.admin_validacion_pagos, name="admin_validacion_pagos"),
    path('home/administrar/torres/', views.admin_torres, name="admin_torres"),
    path('home/administrar/noticias/', views.admin_noticias, name="admin_noticias"),
    path('home/administrar/cuentas/', views.admin_cuentas, name="admin_cuentas"),
    path('home/administrar/reportes/', views.admin_reportes, name="admin_reportes"),
    path('home/administrar/cierres/', views.admin_cierres, name="admin_cierres"),
    path('home/administrar/configuracion/<str:type>', views.admin_configuracion, name="admin_configuracion"),
    path('home/administrar/configuracion/domicilios/', views.admin_domicilios, name="admin_domicilios"),
    path('home/administrar/reservacion/', views.reservacion, name='reservacion'),
    path('home/administrar/reservacion/<id_alquiler>/', views.reserva, name='reservacion'),
    
    #path('home/administrar/reservacion_list/', views.reservacion_list, name='reservacion_list'),

    # URLS de configuracion del edificio
    path('home/administrar/configuracion/recargos-y-descuentos/', views.configuracion_recargos_descuentos, name="configurar_recargos_y_descuentos"),
    path('home/administrar/configuracion/tasas-de-cambio/', views.configuracion_tasas_de_cambio, name="tasas_de_cambio"),
    path('home/administrar/configuracion/establecer-precios/', views.configuracion_establecimiento_precios, name="establecimiento_precios"),

    # READ
    path('home/administrar/bancos/ver/<int:id>', views.readBancos, name="readBancos"),
    path('home/administrar/gastos/ver/<int:id>', views.readGastos, name="readGastos"),
    path('home/administrar/ingresos/ver/<int:id>', views.readIngresos, name="readIngresos"),
    path('home/administrar/pagos/ver/<int:id>', views.readPagoMovimiento, name="readPagoMovimiento"),
    path('home/administrar/deudas/ver/<int:id>', views.readDeudas, name="readDeudas"),
    path('home/administrar/deudas/ver/propietario/<int:id>/<id_propietario>', views.readPropDeudas, name="readPropDeudas"),
    path('home/administrar/propietarios/ver/<int:id>', views.readPropietarios, name="readPropietarios"),
    path('home/administrar/cuentas/ver/<int:id>', views.readCuentas, name="readCuentas"),

    # UPDATE
    path('home/administrar/bancos/actualizar/<int:id>', views.updateBancos, name="updateBancos"),
    path('home/administrar/gastos/actualizar/<int:id>', views.updateGastos, name="updateGastos"),
    path('home/administrar/ingresos/actualizar/<int:id>', views.updateIngresos, name="updateIngresos"),
    path('home/administrar/deudas/actualizar/<int:pk>', views.DeudasUpdateView.as_view(), name="updateDeudas"),
    path('home/administrar/propietarios/actualizar/<int:id>', views.updatePropietarios, name="updatePropietarios"),
    path('home/administrar/cuentas/actualizar/<int:id>', views.updateCuentas, name="updateCuentas"),
    path('home/administrar/noticias/actualizar/<slug>', views.updateNoticia, name="updateNoticia"),
    path('home/administrar/torres/actualizar/<int:id>', views.updateTorres, name="updateTorres"),
    path('home/administrar/domicilio/actualizar/<id_domicilio>', views.updateDom, name="updateDom"),
    # path('home/administrar/domicilio/actualizar/<int:id>', views.updateDom, name="updateDom"),

    # DELETE
    path('home/administrar/bancos/eliminar/<int:id>', views.destroyBancos, name="destroyBancos"),
    path('home/administrar/gastos/eliminar/<int:id>', views.destroyGastos, name="destroyGastos"),
    path('home/administrar/ingresos/eliminar/<int:id>', views.destroyIngresos, name="destroyIngresos"),
    path('home/administrar/deudas/eliminar/<int:id>', views.destroyDeudas, name="destroyDeudas"),
    path('home/administrar/propietarios/eliminar/<int:id>', views.destroyPropietarios, name="destroyPropietarios"),
    path('home/administrar/cuentas/eliminar/<int:id>', views.destroyCuenta, name="destroyCuentas"),
    path('home/administrar/noticia/eliminar/<slug>', views.destroyNoticia, name="destroyNoticia"),
    path('home/administrar/torres/eliminar/<int:id>', views.destroyTorres, name="destroyTorres"),
    path('home/administrar/domicilio/eliminar/<int:id>', views.destroyDom, name="destroyDom"),

    #DOWNLOAD
    path('home/administrar/gastos/ver/referencia', views.downloadReferencia, name="downloadReferencia"),
    path('home/administrar/gastos/ver/referenciaI', views.downloadReferenciaingreso, name="downloadReferenciaingreso"),

    # UTILS
    path('home/administrar/propietarios/enviar_email/<int:id>', views.enviar_email, name="enviar_email"),
    path('obtener_pisos/', views.obtener_pisos, name='obtener_pisos'),
    path('obtener_bancos/', views.obtener_bancos, name='obtener_bancos'),
    path('admin_propietarios_mov/', views.admin_propietarios_mov, name='admin_propietarios_mov'),
    path('cierre_propietario/', views.cierre_propietario, name='cierre_propietario'),
    path('obtener_deudas/', views.obtener_deudas, name='obtener_deudas'),
    path('eliminar_publicacion/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('cambiar_monto/', views.cambiar_monto, name='cambiar_monto'),
    path('obtener_domicilio/', views.obtener_domicilio, name='obtener_domicilio'),
    path('enviar-consulta/', views.enviar_consulta, name="enviar_consulta"),
    path('cerrar-sesion/', views.cerrar_sesion, name="cerrar_sesion"),
    path('inicio/', views.redireccion_de_usuario, name="redireccion"),

    path('agregar_elemento/', views.agregar_elemento, name="agregar_elemento"),
    # path('eliminar_elemento/', views.eliminar_elemento, name="eliminar_elemento"),
    # path('eliminar_db/', views.limpiar_db, name="eliminar_todo"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)