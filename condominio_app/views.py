from django.urls import reverse_lazy
import urllib3
from bs4 import BeautifulSoup
import requests
from django.db.models.functions import Extract, TruncMonth
from django.shortcuts import render 
import csv
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect, FileResponse
import json
from currency_converter import CurrencyConverter
from django.utils.translation import template
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import View
from django.core.files.base import ContentFile
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.utils import timezone
from django.db import transaction
from django.db.models import Q, Sum, Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datetime import date, datetime, timedelta, time
from decimal import Decimal
from random import randint, seed
from faker import Faker
from operator import attrgetter
from condominio import settings
from .models import Rol as RolModel
from .models import *
from .forms import *
# from weasyprint import HTML, CSS  # DESACTIVADO - Windows GTK
from django.contrib.auth.hashers import make_password
import time
import random
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from cryptography.fernet import Fernet
from django.shortcuts import redirect
from reportlab.pdfgen import canvas
from django.http import FileResponse
import io
from django.views.generic import DetailView
from django.db.models import Q
from datetime import datetime, date, timedelta
from django.conf import settings
from django.http import HttpResponse
import django
from urllib.parse import urlparse
import condominio.settings as cs
import sys

def check_static(request):
    print("DJANGO:", django.get_version(), file=sys.stderr)
    print("STATIC_URL settings de django.conf:", settings.STATIC_URL, file=sys.stderr)


def get_back_url(request, fallback):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return fallback
    parsed = urlparse(referer)
    if parsed.netloc and parsed.netloc != request.get_host():
        return fallback
    path = parsed.path or ''
    if not path.startswith('/'):
        return fallback
    if parsed.query:
        return f"{path}?{parsed.query}"
    return path
    print("STATIC_URL settings de condominio.settings:", cs.STATIC_URL, file=sys.stderr)
    print("condominio.settings.__file__:", cs.__file__, file=sys.stderr)

    info = (
        f"STATIC_URL (django.conf): {settings.STATIC_URL}<br>"
        f"STATIC_URL (condominio.settings): {cs.STATIC_URL}<br>"
        f"STATIC_ROOT: {getattr(settings, 'STATIC_ROOT', None)}"
    )
    return HttpResponse(info)

def check_settings(request):
    info = (
        f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'No definido')}<br>"
        f"settings module: {settings.__module__}<br>"
        f"STATIC_URL: {settings.STATIC_URL}<br>"
        f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', None)}<br>"
        f"FORCE_SCRIPT_NAME: {getattr(settings, 'FORCE_SCRIPT_NAME', None)}<br>"
    )
    # También lo mandamos a logs
    print("DJANGO_SETTINGS_MODULE:", os.environ.get("DJANGO_SETTINGS_MODULE", "No definido"), file=sys.stderr)
    print("settings module:", settings.__module__, file=sys.stderr)
    print("STATIC_URL:", settings.STATIC_URL, file=sys.stderr)
    print("MEDIA_URL:", getattr(settings, "MEDIA_URL", None), file=sys.stderr)
    print("FORCE_SCRIPT_NAME:", getattr(settings, "FORCE_SCRIPT_NAME", None), file=sys.stderr)

    return HttpResponse(info)

def check_database(request):
    """Vista para verificar la conexión a la base de datos"""
    from django.db import connection
    from django.conf import settings
    from condominio_app.models import Usuario
    
    db_info = []
    db_info.append("<h2>Información de la Base de Datos</h2>")
    db_info.append(f"<p><strong>Engine:</strong> {settings.DATABASES['default']['ENGINE']}</p>")
    db_info.append(f"<p><strong>Name:</strong> {settings.DATABASES['default']['NAME']}</p>")
    db_info.append(f"<p><strong>Host:</strong> {settings.DATABASES['default']['HOST']}</p>")
    db_info.append(f"<p><strong>User:</strong> {settings.DATABASES['default']['USER']}</p>")
    db_info.append(f"<p><strong>Port:</strong> {settings.DATABASES['default']['PORT']}</p>")
    
    try:
        # Intentar conectar a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            db_info.append(f"<p style='color: green;'><strong>✅ Conexión exitosa!</strong></p>")
            db_info.append(f"<p><strong>Versión PostgreSQL:</strong> {version}</p>")
            
            # Verificar si hay usuarios usando el modelo
            user_count = Usuario.objects.count()
            db_info.append(f"<p><strong>Usuarios en la base de datos:</strong> {user_count}</p>")
            
            if user_count > 0:
                users = Usuario.objects.all()[:10]
                db_info.append("<h3>Usuarios encontrados:</h3>")
                db_info.append("<table border='1' style='border-collapse: collapse; padding: 5px;'>")
                db_info.append("<tr><th>ID</th><th>Username</th><th>Email</th><th>Rol ID</th><th>Condominio ID</th><th>is_superuser</th><th>is_active</th></tr>")
                for user in users:
                    db_info.append(f"<tr><td>{user.id}</td><td>{user.username}</td><td>{user.email}</td><td>{user.id_rol_id}</td><td>{user.id_condominio_id}</td><td>{user.is_superuser}</td><td>{user.is_active}</td></tr>")
                db_info.append("</table>")
                db_info.append("<p><strong>Nota:</strong> Para probar login, usa el username exacto (puede estar en mayúsculas)</p>")
            else:
                db_info.append("<p style='color: orange;'><strong>⚠️ No hay usuarios en la base de datos.</strong></p>")
                db_info.append("<p>Necesitas crear un superusuario con: <code>python manage.py create_admin</code></p>")
                
    except Exception as e:
        db_info.append(f"<p style='color: red;'><strong>❌ Error al conectar:</strong> {str(e)}</p>")
        db_info.append(f"<p><strong>Tipo de error:</strong> {type(e).__name__}</p>")
        import traceback
        db_info.append(f"<pre>{traceback.format_exc()}</pre>")
        db_info.append("<h3>Posibles soluciones:</h3>")
        db_info.append("<ul>")
        db_info.append("<li>Verifica que el servidor PostgreSQL esté corriendo</li>")
        db_info.append("<li>Verifica que las credenciales sean correctas</li>")
        db_info.append("<li>Verifica que el firewall permita la conexión al puerto 5432</li>")
        db_info.append("<li>Verifica que puedas alcanzar el host 159.203.165.120</li>")
        db_info.append("</ul>")
    
    return HttpResponse("".join(db_info))

def reservacion(request):
   
    
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    
    reservacion = Reservacion()
    hoy = date.today()
    fecha_minima = hoy
    fecha_maxima = hoy + timedelta(days=1825)  # 5 años a partir de hoy
    
    context = {
       'hoy': hoy,
    }
    if request.method == 'POST':
        print(request.POST)
        reservacion.nombre = request.POST['Nombres']
        reservacion.apellido = request.POST['Apellidos']
        reservacion.cedula = request.POST['Cedula']
        reservacion.telefono = request.POST['Telefono']
        reservacion.Banco = request.POST['Banco']
        reservacion.referenncia_bancaria = request.POST['Referencia_bancaria']
        reservacion.Fecha_entrada = datetime.strptime(request.POST['Fecha_entrada'], '%Y-%m-%d').date()
        reservacion.Fecha_salida = datetime.strptime(request.POST['Fecha_salida'], '%Y-%m-%d').date()
        reservacion.soporte_pago = request.FILES['soporte_pago']
        Fecha_entrada = reservacion.Fecha_entrada
        Fecha_salida = reservacion.Fecha_salida
        

#Trae el id del alquiler que se quiere reservar
def  reserva(request, id_alquiler): 
    reservacion = Reservacion.objects.all()
    alquiler = Alquiler.objects.get(id_alquiler=id_alquiler)

    return render(request, 'administrador/reservaciones.html', {'reservacion': reservacion, 'alquiler':alquiler})

def reservacion(request):
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    
    reservacion = Reservacion()
    hoy = date.today()
    fecha_minima = hoy
    fecha_maxima = hoy + timedelta(days=1825)  # 5 años a partir de hoy
    
    context = {
       'hoy': hoy.strftime('%Y-%m-%d'), 
    }
    
    if request.method == 'POST':
        print(request.POST)
        
         # Obtener la instancia de Alquiler correspondiente al ID
        id_alquiler = request.POST['txtId_alquiler']
        try:
            alquiler = Alquiler.objects.get(id_alquiler=id_alquiler)  # Cambia 'id' por el campo correcto si es necesario
        except Alquiler.DoesNotExist:
            error_message = "El alquiler especificado no existe."
            return render(request, 'administrador/reservaciones.html', {'error_message': error_message})
        
        reservacion.id_alquiler = alquiler  # Asigna la instancia de Alquiler
        reservacion.nombre = request.POST['Nombres']
        reservacion.apellido = request.POST['Apellidos']
        reservacion.cedula = int(request.POST['Cedula'])
        reservacion.telefono = int(request.POST['Telefono'])
        reservacion.Banco = request.POST['Banco']
        reservacion.referenncia_bancaria = int(request.POST['Referencia_bancaria'])
        reservacion.Fecha_entrada = datetime.strptime(request.POST['Fecha_entrada'], '%Y-%m-%d').date()
        reservacion.Fecha_salida = datetime.strptime(request.POST['Fecha_salida'], '%Y-%m-%d').date()
        reservacion.soporte_pago = request.FILES['soporte_pago']
        Fecha_entrada = reservacion.Fecha_entrada.strftime('%Y-%m-%d')
        Fecha_salida = reservacion.Fecha_salida.strftime('%Y-%m-%d')
        
        if reservacion.Fecha_entrada < fecha_minima or reservacion.Fecha_entrada > fecha_maxima or  reservacion.Fecha_salida < fecha_minima or reservacion.Fecha_salida > fecha_maxima:
            # Mostrar un mensaje de error
            error_message = "Las fechas deben estar dentro del rango permitido (hoy a 5 años a partir de hoy)."
            return render(request, 'administrador/reservaciones.html', {'error_message': error_message})
        reservacion.save()
    messages.success(request, '¡El usuario ha sido registrado de manera satisfactoria!', extra_tags='alert-success')
    return render(request, 'administrador/reservaciones.html', context)
     



def añadir_alquiler(request):

    alquiler = Alquiler()
    alq = Alquiler.objects.all()
    if request.method == 'POST': 
        alquiler.tipo_post = request.POST['txtTipoPost']
        alquiler.categoria_post = request.POST['txtCatPost']
        alquiler.titulo = request.POST['txtTitulo']
        alquiler.descripcion = request.POST['txtDescripcion']
        alquiler.horario_desde = request.POST['txtDesde']
        alquiler.horario_hasta = request.POST['txtHasta']
        alquiler.imagen = request.FILES['txtImgAlquiler']
        alquiler.contacto = request.POST['txtContacto']
        alquiler.is_active = request.POST['txtIsActive']
        alquiler.save()
   
    #if  request.method == 'POST':
     #   publicaciones_form = PublicacionesForm(data=request.POST)

      #  if publicaciones_form.is_valid():
        #    publicaciones_form.save()
       #     return HttpResponseRedirect(reverse('condominio_app:añadir_alquiler')+'?ok')
        #else:
        #    return HttpResponseRedirect(reverse('condominio_app:añadir_alquiler')+'?error')

    return render(request, 'administrador/añadir_alquiler.html', {'alq': alq})

#REDIRECCIONAR A ALQUILERES
def alquileresRedic(request):
    alq_list = Alquiler.objects.all().order_by('-id_alquiler')
    paginator = Paginator(alq_list, 10)
    page_number = request.GET.get('page')
    alq = paginator.get_page(page_number)
    return render(request, 'visitante/alquileres.html', {'alq': alq})
 
#REDIRECCIONAR A RESERVACIONES
def reservacionesRedic(request):
     return render(request, 'administrador/reservaciones.html')

#REDIRECCIONAR A confirmacion de reservaciones
def conf_reserva(request):

    hoy = timezone.now()
    datos = Reservacion.objects.all()
    paginator = Paginator(datos, 2)  # Mostrar 10 alquileres por página

    page_number = request.GET.get('page')  # Obtén el número de página de la solicitud
    alq = paginator.get_page(page_number)  # Obtén la página actual
    local_data = ['venezuela', 'Banesco', 'Mercantil'] 
    mensajes = []
    

    reservaciones_vencidas = datos.filter(Fecha_salida__lte=hoy)

    for reservacion in reservaciones_vencidas:
        reservacion.estado = False
        reservacion.save()
        
        if reservacion.id_alquiler:  # Verifica si hay un alquiler relacionado
            alquiler = reservacion.id_alquiler  # Accede al objeto Alquiler
            alquiler.estado = False  # Sincroniza el estado
            alquiler.save()
            mensajes.append(f'¡La reservación del usuario {reservacion.nombre} ha caducado!')

    # Agregar mensajes a la sesión
    for mensaje in mensajes:
        messages.success(request, mensaje, extra_tags='alert-success')

    
    
    return render(request, 'administrador/conf_reserva.html', {'datos': datos, 'local_data': local_data, 'alq':alq})
 
 #CAMBIAR ESTADO **************************************
 
def update_view(request, id_reservacion):
    reservacion = Reservacion.objects.get(id_reservacion=id_reservacion)
    reservacion.Fecha_entrada = reservacion.Fecha_entrada.strftime('%Y-%m-%d')
    reservacion.Fecha_salida = reservacion.Fecha_salida.strftime('%Y-%m-%d') 
    
    return render(request,'administrador/conf_estado.html', {'reservacion':reservacion})  
                
def editarEstado(request):
    estado = request.POST['txtestado']
    Nombre = request.POST['txtNombre']
    Cedula = request.POST['txtCedula']
    Referencia = request.POST['txtReferencia']
    Id_reservacion = request.POST['txtidreservacion']

    reservacion = Reservacion.objects.get(id_reservacion=Id_reservacion)
    reservacion.estado = estado
    reservacion.nombre = Nombre
    reservacion.cedula = Cedula
    reservacion.referenncia_bancaria = Referencia
    reservacion.id_reservacion = Id_reservacion
    reservacion.save()

    # Si tienes un modelo Alquiler relacionado, actualiza su estado
    if reservacion.id_alquiler:  # Verifica si hay un alquiler relacionado
        alquiler = reservacion.id_alquiler  # Accede al objeto Alquiler
        alquiler.estado = estado  # Sincroniza el estado
        alquiler.save()

    messages.success(request, f'¡La solicitud del usuario {reservacion.nombre} ha sido aprobada satisfactoria!', extra_tags='alert-success')
    return HttpResponseRedirect(reverse('condominio_app:conf_reserva'))
            
#---------------------------------envia datos a el template reservaciones-----------------------------------  



# PARA GENERAR PDF
from django_xhtml2pdf.utils import generate_pdf
from xhtml2pdf import pisa

# from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
# from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCaptureRequest

import sys, json, psycopg2, os, array

fakegen = Faker()

# En esto se define el número de publicaciones que se verán por página en el apartado de cartelera informativa
NOTICIAS_PER_PAGE = 3


# Create your views here.

# ------------------------------PÁGINA DE INICIO------------------------------

def _tipo_panel_usuario(user):
    """
    Una sola fuente de verdad para evitar bucles. Usa SOLO datos recién leídos de la BD.
    - Cualquier is_superuser=True → 'superuser' (evita bucles con HEADADMIN)
    - ADMIN (ej. MUTOMBO): rol 0/1, con id_condominio → 'admin'
    - Resto → 'propietario'
    """
    if not user or not getattr(user, 'is_authenticated', False):
        return None
    try:
        u = Usuario.objects.select_related('id_rol').get(pk=user.pk)
    except (Usuario.DoesNotExist, AttributeError):
        return 'propietario'
    # Primero: cualquier superuser va al panel superuser (evita bucles HEADADMIN → propietarios)
    if getattr(u, 'is_superuser', False):
        return 'superuser'
    tiene_condominio = u.id_condominio_id is not None
    rol_val = getattr(getattr(u, 'id_rol', None), 'rol', None)
    es_rol_admin = rol_val is not None and str(rol_val) in ('0', '1')
    if es_rol_admin:
        if tiene_condominio:
            return 'admin'
        return 'admin'
    return 'propietario'


def iniciar_sesion(request):
    form = AccountAuthenticationForm(request.POST)
    username = request.POST.get('username', '').upper()
    password = request.POST.get('password', '')
    
    if not username or not password:
        return None
    
    user = authenticate(username=username, password=password)
    print(user)

    if user:
        login(request, user)
        tipo = _tipo_panel_usuario(user)
        if tipo == 'superuser':
            return 'superuser'
        if tipo == 'admin':
            return True
        return False
    else:
        print("El usuario no se encuentra registrado en el sistema.")
        return None

@ensure_csrf_cookie
def home(request):
    """Página inicial: solo login. Si ya está autenticado, redirige a su panel o al inicio de su condominio."""
    if request.user.is_authenticated:
        tipo = _tipo_panel_usuario(request.user)
        if tipo == 'superuser':
            return HttpResponseRedirect(reverse('condominio_app:home_superuser'))
        if tipo == 'admin' or tipo == 'propietario':
            return HttpResponseRedirect(reverse('condominio_app:inicio_condominio'))

    if request.method == 'POST' and 'username' in request.POST:
        usuario = iniciar_sesion(request)
        if usuario == 'superuser':
            return HttpResponseRedirect(reverse('condominio_app:home_superuser'))
        if usuario is True:
            return HttpResponseRedirect(reverse('condominio_app:inicio_condominio'))
        if usuario is False:
            return HttpResponseRedirect(reverse('condominio_app:inicio_condominio'))
        messages.error(request, 'Usuario y/o contraseña incorrecta. Verifique e intente de nuevo.',
                      extra_tags='alert-danger')

    return render(request, 'visitante/login.html')


@login_required
def inicio_condominio(request):
    """Pantalla de inicio del condominio (banners y nombre). Tras login, admin y propietario ven la de su condominio."""
    user = request.user
    tipo = _tipo_panel_usuario(user)
    if tipo == 'superuser':
        return HttpResponseRedirect(reverse('condominio_app:home_superuser'))

    condominio = None
    if tipo == 'admin':
        condominio = getattr(user, 'id_condominio', None)
    else:
        # Propietario no tiene id_condominio; se obtiene del primer Domicilio
        prop = Propietario.objects.filter(id_usuario_id=user.pk).first()
        if prop:
            dom = Domicilio.objects.filter(id_propietario_id=prop.id_propietario).select_related('id_condominio').first()
            if dom:
                condominio = dom.id_condominio

    if not condominio:
        if tipo == 'propietario':
            return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))
        return HttpResponseRedirect(reverse('condominio_app:home'))

    from django.contrib.staticfiles.storage import staticfiles_storage
    b1 = condominio.banner_1.url if condominio.banner_1 else staticfiles_storage.url('img/banner/banner.png')
    b2 = condominio.banner_2.url if condominio.banner_2 else staticfiles_storage.url('img/banner/banner2.png')
    b3 = condominio.banner_3.url if condominio.banner_3 else staticfiles_storage.url('img/banner/banner3.png')
    b4 = staticfiles_storage.url('img/banner/banner4.png')

    return render(request, 'visitante/inicio_condominio.html', {
        'condominio': condominio,
        'tipo_usuario': tipo,
        'banner_1_url': b1,
        'banner_2_url': b2,
        'banner_3_url': b3,
        'banner_4_url': b4,
    })


@login_required
def home_superuser(request):
    """HEADADMIN: listar, crear y eliminar condominios. Solo si tipo es 'superuser' (is_superuser)."""
    user = request.user
    # Evitar bucle: si es superuser sin condominio, no redirigir nunca a propietarios
    if getattr(user, 'is_superuser', False) and getattr(user, 'id_condominio_id', None) is None:
        tipo = 'superuser'
    else:
        tipo = _tipo_panel_usuario(user)
    if tipo != 'superuser':
        if tipo == 'admin':
            return HttpResponseRedirect(reverse('condominio_app:home_admin'))
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominios = Condominio.objects.all().order_by('nombre_condominio')
    # Rol de administrador: mismo que usan MUTOMBO, BIGBLACK y cualquier condominio
    rol_admin = RolModel.objects.filter(rol='0').first() or RolModel.objects.filter(rol='1').first() or RolModel.objects.filter(id_rol__in=[0, 1]).first()

    # POST: crear condominio + admin
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'crear':
            nombre = (request.POST.get('nombre_condominio') or '').strip()
            rif = (request.POST.get('rif_condominio') or '').strip()
            direccion = (request.POST.get('direccion_condominio') or '').strip()
            tipo_condominio = (request.POST.get('tipo_condominio') or '').strip() or None
            email_condo = (request.POST.get('email_condominio') or '').strip()
            codigo_tlf = (request.POST.get('codigo_tlf_1') or '0').strip()
            tlf = (request.POST.get('tlf_1') or '-').strip()
            admin_username = (request.POST.get('admin_username') or '').strip().upper()
            admin_email = (request.POST.get('admin_email') or '').strip()
            admin_password = request.POST.get('admin_password') or ''

            if not nombre or not rif or not direccion:
                messages.error(request, 'Nombre, RIF y dirección del condominio son obligatorios.', extra_tags='alert-danger')
            elif not tipo_condominio:
                messages.error(request, 'Debe seleccionar el tipo de condominio (Apartamentos, Casas o Comercial).', extra_tags='alert-danger')
            elif not admin_username or not admin_email or not admin_password:
                messages.error(request, 'Usuario, email y contraseña del administrador son obligatorios.', extra_tags='alert-danger')
            elif Usuario.objects.filter(username=admin_username).exists():
                messages.error(request, f'Ya existe un usuario con nombre "{admin_username}".', extra_tags='alert-danger')
            else:
                try:
                    with transaction.atomic():
                        # Si no existe rol admin en BD (ej. instalación nueva), crear uno para que todos los condominios funcionen igual
                        if not rol_admin:
                            rol_admin, _ = RolModel.objects.get_or_create(rol='0', defaults={'rol': '0'})
                        condominio = Condominio.objects.create(
                            nombre_condominio=nombre,
                            rif_condominio=rif,
                            direccion_condominio=direccion,
                            tipo_condominio=tipo_condominio,
                            email=admin_email if not email_condo else email_condo,
                            codigo_tlf_1=codigo_tlf or '0',
                            tlf_1=tlf or '-',
                        )
                        admin_user = Usuario.objects.create_user(
                            username=admin_username,
                            email=admin_email,
                            password=admin_password,
                        )
                        admin_user.id_condominio = condominio
                        admin_user.id_rol = rol_admin
                        admin_user.save()
                    messages.success(request, f'Condominio "{nombre}" y administrador "{admin_username}" creados correctamente.', extra_tags='alert-success')
                except Exception as e:
                    messages.error(request, f'Error al crear: {str(e)}', extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:home_superuser'))

        if accion == 'eliminar':
            pk = request.POST.get('id_condominio')
            if pk:
                try:
                    with transaction.atomic():
                        Usuario.objects.filter(id_condominio_id=pk).update(id_condominio=None)
                        Condominio.objects.filter(pk=pk).delete()
                    messages.success(request, 'Condominio eliminado.', extra_tags='alert-success')
                except Exception as e:
                    messages.error(request, f'No se pudo eliminar: {str(e)}', extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:home_superuser'))

    return render(request, 'superuser/home_superuser.html', {
        'condominios': condominios,
    })


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('/')


# ------------------------------VIVIENDAS Y LOCALES COMERCIALES EN ALQUILER O VENTA------------------------------
def viviendas(request):
    # INICIO DE SESIÓN
    if request.POST:
        usuario = iniciar_sesion(request)
        if usuario:
            return HttpResponseRedirect(reverse('condominio_app:home_admin'))
        else:
            return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))
    else:
        form = AccountAuthenticationForm()

    posts = Alquiler.objects.filter(is_active=True, categoria_post="RESIDENCIAL").select_related(
        'id_domicilio__id_propietario')

    paginator = Paginator(posts, 6)
    numero_pagina = request.GET.get('pagina')
    pagina_actual = paginator.get_page(numero_pagina)

    return render(request, 'visitante/viviendas.html', {'pagina_actual': pagina_actual, 'posts': posts})

def alquiler_residencial(request):
    # INICIO DE SESIÓN
    if request.POST:
        usuario = iniciar_sesion(request)
        if usuario:
            return HttpResponseRedirect(reverse('condominio_app:home_admin'))
        else:
            return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))
    else:
        form = AccountAuthenticationForm()

    posts = Alquiler.objects.filter(is_active=True, categoria_post="RESIDENCIAL").select_related('id_domicilio')
    domicilios = []

    for post in posts:
        domicilios.append(Domicilio.objects.select_related('id_torre').get(id_domicilio=post.id_domicilio_id))

    data_post = zip(posts, domicilios)

    paginator = Paginator(posts, 6)
    numero_pagina = request.GET.get('pagina')
    pagina_actual = paginator.get_page(numero_pagina)

    return render(request, 'visitante/alquiler_residencial.html', {'pagina_actual': pagina_actual, 'data_post': data_post})

def alquiler_vacacional(request):
    # INICIO DE SESIÓN
    if request.POST:
        usuario = iniciar_sesion(request)
        if usuario:
            return HttpResponseRedirect(reverse('condominio_app:home_admin'))
        else:
            return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))
    else:
        form = AccountAuthenticationForm()

    posts = Alquiler.objects.filter(is_active=True, categoria_post="VACACIONAL").select_related('id_domicilio')

    paginator = Paginator(posts, 6)
    numero_pagina = request.GET.get('pagina')
    pagina_actual = paginator.get_page(numero_pagina)

    return render(request, 'visitante/alquiler_vacacional.html', {'pagina_actual': pagina_actual, 'posts': posts})


def local_comercial(request):
    # INICIO DE SESIÓN
    if request.POST:
        usuario = iniciar_sesion(request)
        if usuario:
            return HttpResponseRedirect(reverse('condominio_app:home_admin'))
        else:
            return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))
    else:
        form = AccountAuthenticationForm()

    posts = Alquiler.objects.filter(is_active=True, categoria_post="COMERCIAL").select_related(
        'id_domicilio__id_propietario')

    paginator = Paginator(posts, 6)
    numero_pagina = request.GET.get('pagina')
    pagina_actual = paginator.get_page(numero_pagina)

    return render(request, 'visitante/local_comercial.html', {'pagina_actual': pagina_actual, 'posts': posts})


# ------------------------------SOBRE NOSOTROS------------------------------
def sobre_nosotros(request):
    # INICIO DE SESIÓN
    if request.POST:
        usuario = iniciar_sesion(request)
        if usuario:
            return HttpResponseRedirect(reverse('condominio_app:home_admin'))
        else:
            return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))
    else:
        form = AccountAuthenticationForm()

    return render(request, 'visitante/about.html')


# ------------------------------CARTELERA INFORMATIVA------------------------------
def cartelera_informativa(request):
    # INICIO DE SESIÓN
    if request.POST:
        usuario = iniciar_sesion(request)
        if usuario:
            return HttpResponseRedirect(reverse('condominio_app:home_admin'))
        else:
            return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))
    else:
        form = AccountAuthenticationForm()

    context = {}
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    # Filtro de noticias con un rango de 6 días DEBE LIMITARSE A MOSTRAR SOLO 6 PUBLICACIONES
    startdate = datetime.today()
    enddate = startdate - timedelta(days=6)
    recent_posts = Noticia.objects.filter(fecha_publicacion__range=[enddate, startdate]).order_by('-fecha_actualizado')
    context['recent_posts'] = recent_posts

    noticias = sorted(get_publicacion_queryset(query), key=attrgetter('fecha_actualizado'), reverse=True)

    page = request.GET.get('page', 1)
    noticias_paginator = Paginator(noticias, NOTICIAS_PER_PAGE)

    try:
        noticias = noticias_paginator.page(page)
    except PageNotAnInteger:
        noticias = noticias_paginator.page(NOTICIAS_PER_PAGE)
    except EmptyPage:
        noticias = noticias_paginator.page(noticias.paginator.num_pages)

    context['noticias'] = noticias

    return render(request, 'visitante/cartelera.html', context)


def contacto(request):
    # INICIO DE SESIÓN
    if request.POST:
        usuario = iniciar_sesion(request)
        if usuario:
            return HttpResponseRedirect(reverse('condominio_app:home_admin'))
        else:
            return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))
    else:
        form = AccountAuthenticationForm()

    context = {}
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    return render(request, 'visitante/contacto.html')

@require_POST
def send_mail(request):
    if request.method == 'POST':

        dataEmail = {
            'nombre': request.POST['nombre'],
            'email': request.POST['email'],
            'asunto': request.POST['asunto'],
            'body': request.POST['body']
        }

        html_content = render_to_string('mails/consulta_mail.html', dataEmail)

        email = EmailMultiAlternatives('Esparta Suites: Consulta', html_content)
        email.attach_alternative(html_content, "text/html")
        email.to = [settings.EMAIL_HOST_USER]
        res = email.send()
        if (res == 1):
            print("Correo enviado satisfactoriamente")
            return redirect('/contacto')
    # messages.success(request, '¡El email ha sido enviado correctamente!', extra_tags='alert-success')
    # return HttpResponseRedirect(reverse('condominio_app:home_admin'))

    return render(request, 'visitante/contacto.html')



# ------------------------------VISTA DE PUBLICACIÓN EN ESPECIFICO------------------------------
def noticia(request, slug):
    publicacion = get_object_or_404(Noticia, slug=slug)
    total_noticias = Noticia.objects.all().count()
    todas_las_noticias = Noticia.objects.all()

    # Variables para definir los rangos de fecha
    start = timezone.now()
    end = start - timezone.timedelta(days=7)

    # Se acomodan las publicaciones recientes por la fecha de actualización
    recent_posts = Noticia.objects.filter(fecha_actualizado__gte=end).order_by('-fecha_actualizado')

    previous_pub = None
    next_pub = None
    if total_noticias > 1:
        seed(1)

        # Publicacion anterior y siguiente publicacion
        if publicacion.id - 1 == 0:
            previous_pub = None
        else:
        

            previous_pub = get_object_or_404(Noticia, id=publicacion.id)

        try:
            next_post = get_object_or_404(Noticia, id=publicacion.id + 1)
            print("si hay otra publicacion despues de esta")

            next_pub = get_object_or_404(Noticia, id=next_post.id)
        except:
            print("ya no hay más publicaciones despues de esta")
            next_pub = None

    return render(request, 'visitante/read_noticia.html',
                  {'publicacion': publicacion, 'previous_post': previous_pub, 'next_post': next_pub,
                   'recent_posts': recent_posts})


# A partir de aquí iran las vistas del modulo del propietario
# ------------------------------VISTAS PROPIETARIO------------------------------

@login_required
def home_propietarios(request):
    user = request.user
    tipo = _tipo_panel_usuario(user)
    if tipo == 'admin':
        return HttpResponseRedirect(reverse('condominio_app:home_admin'))
    if tipo == 'superuser':
        return HttpResponseRedirect(reverse('condominio_app:home_superuser'))
    propietarios = Propietario.objects.filter(id_usuario_id=user.id).first()
    if not propietarios:
        return HttpResponseRedirect(reverse('condominio_app:home_admin'))
    domicilios = Domicilio.objects.filter(id_propietario_id=propietarios.id_propietario)

    return render(request, 'propietarios/home_propietarios.html', {'user': propietarios, 'propietario': propietarios,
                                                                   'domicilios': domicilios})

def confirmarPago(request, ids, prop):

    try:
        banco_receptor = Bancos.objects.get(
            id_banco=request.POST['bancoReceptor'],
            id_condominio_id=request.user.id_condominio_id
        )
    except Bancos.DoesNotExist:
        messages.warning(request, 'El banco receptor seleccionado no es válido para su condominio.',
                         extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:propietarios_pagos'))

    ult_movimiento = Movimientos_bancarios.objects.filter(id_banco_id=banco_receptor.id_banco).last()
    monto_transaccion = Decimal(request.POST['montoPago'])

    concepto_pago = request.POST['descripcion_pago']
    cierre = Cierre_mes.objects.filter(id_condominio_id=request.user.id_condominio_id).order_by('fecha_cierre').last()
    movimientos_qs = Movimientos_bancarios.objects.filter(
        referencia_movimiento=request.POST['Referencia'],
        id_banco_id=banco_receptor.id_banco,
    )
    if cierre:
        movimientos_qs = movimientos_qs.filter(created_at__gt=cierre.fecha_cierre)
    movimiento = movimientos_qs.order_by('-created_at', '-id_movimiento').first()
    if not movimiento:
        debito_val = ult_movimiento.debito_movimiento if ult_movimiento else 0
        credito_val = ult_movimiento.credito_movimiento if ult_movimiento else 0
        movimiento = Movimientos_bancarios.objects.create(
            referencia_movimiento=request.POST['Referencia'],
            fecha_movimiento=request.POST['dateTransferencia'],
            concepto_movimiento=concepto_pago,
            descripcion_movimiento=request.POST['descripcion_pago'],
            debito_movimiento=debito_val,
            credito_movimiento=credito_val,
            monto_movimiento=request.POST['montoPago'],
            banco_emisor=request.POST['bancoEmisor'],
            estado_movimiento=2,
            tipo_moneda=request.POST['moneda_pago'],
            id_banco_id=banco_receptor.id_banco,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    # Asegurar estado pendiente para pagos normales/abonos aunque ya existiera la referencia
    mov_obj = movimiento
    mov_obj.fecha_movimiento = request.POST['dateTransferencia']
    mov_obj.concepto_movimiento = concepto_pago
    mov_obj.descripcion_movimiento = request.POST['descripcion_pago']
    mov_obj.monto_movimiento = request.POST['montoPago']
    mov_obj.banco_emisor = request.POST['bancoEmisor']
    mov_obj.estado_movimiento = 2
    mov_obj.tipo_moneda = request.POST['moneda_pago']
    mov_obj.id_banco_id = banco_receptor.id_banco
    mov_obj.updated_at = timezone.now()
    if not mov_obj.created_at:
        mov_obj.created_at = timezone.now()
    mov_obj.save()

    if not movimiento.concepto_movimiento:
        movimiento.concepto_movimiento = concepto_pago
        movimiento.save()

    ingreso = Ingresos.objects.filter(id_movimiento_id=movimiento.id_movimiento).first()
    if not ingreso:
        ingreso = Ingresos()
    ingreso.tipo_ingreso = 'Pago de un propietario'
    ingreso.id_movimiento_id = movimiento.id_movimiento
    ingreso.id_propietario = prop
    if request.FILES.get('imgReferencia'):
        ingreso.imagen_referencial = request.FILES['imgReferencia']
    ingreso.save()

    Datos_transaccion.objects.get_or_create(nombre_titular=request.POST['nameTitular'],
                                            telefono_titular=request.POST['tlfTitular'],
                                            codigo_area=request.POST['countryCode'],
                                            correo_titular=request.POST['emailTitular'],
                                            tipo_transaccion=request.POST['tipo_transaccion'], id_movimiento_id=movimiento.id_movimiento)

    print(request.POST)

    for id, montos in zip(ids, request.POST.getlist('montos_deudas')):
        print("inicia ciclo for")
        if id == -1:
            print("abono de la deuda")
            guardar_recibo = Recibos(descripcion_recibo=request.POST['descripcion_pago'],
                                     monto=montos, categoria_recibo="ABONO",
                                     fecha_creacion=request.POST['dateTransferencia'],
                                     hora_creacion=datetime.now(),
                                     id_movimiento_id=movimiento.id_movimiento)
            guardar_recibo.save()

        else:
            print("pago")
            deudas = Deudas.objects.get(id_deuda=id)
            if Decimal(montos) <= Decimal(monto_transaccion):
                guardar_recibo = Recibos(descripcion_recibo=deudas.concepto_deuda,
                                         monto=montos, categoria_recibo="SOLVENTE",
                                         fecha_creacion=request.POST['dateTransferencia'],
                                         hora_creacion=datetime.now(),
                                         id_movimiento_id=movimiento.id_movimiento,
                                         id_deuda=deudas)
                guardar_recibo.save()
                print("pago de la deuda")
                deudas.is_active = False
                deudas.save()
                monto_transaccion -= Decimal(montos)

            else:
                monto_abonado = Decimal(montos) - monto_transaccion
                guardar_recibo = Recibos(descripcion_recibo=deudas.concepto_deuda,
                                         monto=monto_abonado, categoria_recibo="ABONADO",
                                         fecha_creacion=request.POST['dateTransferencia'],
                                         hora_creacion=datetime.now(),
                                         id_movimiento_id=movimiento.id_movimiento,
                                         id_deuda=deudas)
                guardar_recibo.save()
                print("pago por abono de la deuda")

    messages.success(request, '¡El pago fue realizado con exito! Por favor espere a que el administrador confirme su transacción.',
                                                  extra_tags='alert-success')
    return HttpResponseRedirect(reverse('condominio_app:propietarios_pagos'))

def pagar_con_saldo(request, ids, prop):
    moneda = request.POST.get('moneda_seleccionada')
    montos = request.POST.getlist('montos_deudas')
    if not moneda or not montos:
        messages.warning(request, 'No se pudo procesar el pago con saldo. Verifique los datos enviados.',
                         extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:propietarios_pagos'))

    deudas = Deudas.objects.filter(id_deuda__in=ids, is_active=True).select_related('id_domicilio')
    deuda = deudas.first()
    if not deuda or not deuda.id_domicilio:
        messages.warning(request, 'No se encontraron deudas válidas para el pago con saldo.',
                         extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:propietarios_pagos'))

    domicilio = deuda.id_domicilio
    total = sum(Decimal(monto) for monto in montos)

    banco = Bancos.objects.filter(
        id_condominio_id=domicilio.id_condominio_id,
        tipo_moneda=moneda
    ).first()
    if not banco:
        messages.warning(request, 'No hay un banco configurado para esa moneda.',
                         extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:propietarios_pagos'))

    if moneda == "USD":
        saldo = domicilio.saldo_usd or 0
    elif moneda == "EUR":
        saldo = domicilio.saldo_eur or 0
    else:
        saldo = domicilio.saldo or 0

    if Decimal(total) > Decimal(saldo):
        messages.warning(request, 'Saldo insuficiente en la moneda seleccionada. Debe pagar normalmente.',
                         extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:propietarios_pagos'))

    if moneda == "USD":
        domicilio.saldo_usd = (domicilio.saldo_usd or 0) - total
    elif moneda == "EUR":
        domicilio.saldo_eur = (domicilio.saldo_eur or 0) - total
    else:
        domicilio.saldo = (domicilio.saldo or 0) - total
    domicilio.save()

    referencia = str(timezone.now()).replace('-', '').replace(':', '').replace('.', '').replace('+', '').replace(' ', '')
    mov = Movimientos_bancarios.objects.create(
        fecha_movimiento=timezone.now().date(),
        concepto_movimiento="Pago con saldo",
        descripcion_movimiento="Pago de deudas con saldo de la cuenta",
        referencia_movimiento=referencia,
        debito_movimiento=0,
        credito_movimiento=0,
        monto_movimiento=total,
        banco_emisor="Saldo de cuenta",
        estado_movimiento=0,
        tipo_moneda=moneda,
        id_banco=banco,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )

    banco.creditos_banco += total
    banco.saldo_actual += total
    banco.ultimo_credito = timezone.now().date()
    banco.save()

    condominio = Condominio.objects.get(id_condominio=domicilio.id_condominio_id)
    if moneda == "USD":
        condominio.saldo_edificio_usd += total
    elif moneda == "EUR":
        condominio.saldo_edificio_eur += total
    else:
        condominio.saldo_edificio += total
    condominio.save()

    ingreso = Ingresos()
    ingreso.tipo_ingreso = 'Pago con saldo'
    ingreso.id_movimiento = mov
    ingreso.id_propietario = domicilio.id_propietario
    ingreso.save()

    for deuda_item in deudas:
        Recibos.objects.create(
            descripcion_recibo=deuda_item.concepto_deuda,
            monto=deuda_item.monto_deuda,
            categoria_recibo="SOLVENTE",
            fecha_creacion=timezone.now().date(),
            hora_creacion=timezone.now(),
            id_movimiento_id=mov.id_movimiento,
            id_deuda=deuda_item
        )
        deuda_item.is_active = False
        deuda_item.updated_at = timezone.now()
        deuda_item.save()

    if not Deudas.objects.filter(id_domicilio=domicilio, is_active=True).exists():
        domicilio.estado_deuda = False
        domicilio.save()

    messages.success(request, '¡La deuda fue pagada con saldo de la cuenta!',
                     extra_tags='alert-success')
    return HttpResponseRedirect(reverse('condominio_app:propietarios_pagos'))

@login_required
def propietarios_pagos(request):
    user = request.user
    # Si el usuario es un administrador entonces se redirige al inicio del administrador
    if user.id_rol and (user.id_rol.rol == '0' or user.id_rol.rol == '1'):
        return HttpResponseRedirect(reverse('condominio_app:home_admin'))
    usuario = Usuario.objects.filter(username=user.username).first()
    propietarios = Propietario.objects.filter(id_usuario_id=user.id).first()
    if not propietarios:
        return HttpResponseRedirect(reverse('condominio_app:home_admin'))
    banco = Bancos.objects.filter(id_condominio=user.id_condominio_id)
    bancos = banco.distinct('tipo_moneda')
    domicilios = Domicilio.objects.filter(id_propietario_id=propietarios.id_propietario)
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        print(request.POST)
        if request.POST['tipo_transaccion'] == 'PAGO':
            ids = request.POST['deudas'].split(',')
            print("confirmar pago: pago")
            confirmarPago(request, ids, propietarios)

        elif request.POST['tipo_transaccion'] == 'ABONO':
            ids = [-1]
            print("confirmar pago: abono")
            confirmarPago(request, ids, propietarios)
        elif request.POST['tipo_transaccion'] == 'SALDO':
            ids = request.POST['deudas'].split(',')
            print("confirmar pago: saldo")
            pagar_con_saldo(request, ids, propietarios)

        else:
            messages.warning(request, 'Hubo un error al concretar el movimiento en el sistema. Por favor intente nuevamente.',
                             extra_tags='alert-danger')

    return render(request, 'propietarios/propietarios_pagos.html', {'user': propietarios, 'propietarios': propietarios,
                                                                    'domicilios': domicilios, 'banco': banco,
                                                                    'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro,
                                                                    'bancos': bancos})


@login_required
def propietario_recibo_pago(request, id):
    user = request.user
    propietarios = Propietario.objects.get(id_usuario_id=user.id)
    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    movimientos = Movimientos_bancarios.objects.select_related('id_banco').get(id_movimiento=id)
    recibos = Recibos.objects.filter(id_movimiento=movimientos.id_movimiento).select_related('id_movimiento')

    # pdf_base = get_template('PDF/recibos_pagos_pdf.html')
    # html_pdf = pdf_base.render(pagos_propietarios.values()[0])

    name_pdf = 'Recibo-' + str(propietarios.nombre_propietario) + '-' + str(movimientos.fecha_movimiento) + '.pdf'

    ruta_logo = os.path.join(os.getcwd(), 'static', 'img-inverdata', 'logo_inverdata_pdf.png')

    nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
    bancos_cabecera = [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in Bancos.objects.filter(id_condominio_id=condominio.id_condominio)]
    html_string = render_to_string('PDF/recibos_pagos_pdf.html', {'datosRecibo': recibos, 'propietarios': propietarios,
                                                                  'datosMovimiento': movimientos, 'datosCondo': condominio,
                                                                  'datos_condominio': condominio, 'fecha_generado': timezone.now(),
                                                                  'bancos_cabecera': bancos_cabecera, 'ruta_logo': ruta_logo})

    # Crear un objeto HTML a partir de la cadena HTML
    # html = HTML(string=html_string, base_url=request.build_absolute_uri())  # DESACTIVADO - Windows GTK

    # Cargar el archivo CSS externo
    # css = CSS(filename='static/css/invoice.css')  # DESACTIVADO - Windows GTK

    # Generar el archivo PDF usando xhtml2pdf (pisa)
    result = io.BytesIO()
    pisa.CreatePDF(html_string, dest=result)
    pdf_file = result.getvalue()

    # Devolver el archivo PDF como respuesta
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="' + name_pdf + '"'
    response.write(pdf_file)

    return response


@login_required
def propietarios_recibos(request):
    user = request.user
    # Si el usuario es un administrador entonces se redirige al inicio del administrador
    if user.id_rol and (user.id_rol.rol == '0' or user.id_rol.rol == '1'):
        return HttpResponseRedirect(reverse('condominio_app:home_admin'))
    propietario = Propietario.objects.get(id_usuario_id=user.id)
    domicilios_propietario = Domicilio.objects.filter(id_propietario_id=propietario.id_propietario)
    recibos_ids = Recibos.objects.filter(id_deuda__id_domicilio__in=domicilios_propietario).values_list('id_movimiento_id', flat=True).distinct()
    pagos_propietarios = Movimientos_bancarios.objects.filter(id_movimiento__in=recibos_ids).distinct()
    cierres = Cierre_mes.objects.filter(id_condominio_id=user.id_condominio_id).order_by('fecha_cierre')

    if request.method == "POST":
        cierre = Cierre_mes.objects.get(id_cierre=request.POST['cierre'])
        pdf_prop = cierre_propietario(request, propietario, cierre, user)
        return pdf_prop

    return render(request, 'propietarios/propietarios_recibos.html', {'user': propietario, 'cierres':cierres,
                                                                      'propietarios': propietario,
                                                                      'movimientos': pagos_propietarios})

@login_required
def propietarios_publicaciones(request):
    user = request.user
    # Si el usuario es un administrador entonces se redirige al inicio del administrador
    if user.id_rol and (user.id_rol.rol == '0' or user.id_rol.rol == '1'):
        return HttpResponseRedirect(reverse('condominio_app:home_admin'))
    propietario = Propietario.objects.filter(id_usuario_id=user.id).first()
    if not propietario:
        return HttpResponseRedirect(reverse('condominio_app:home_admin'))
    inmuebles = Domicilio.objects.filter(id_propietario__id_usuario=user.id)
    posts = []
    domicilios = []
    for domicilio in inmuebles:
        post = Alquiler.objects.filter(id_domicilio_id=domicilio.id_domicilio)
        if post.exists():
            for publicacion in post:
                posts.append(publicacion)
        else:
            domicilios.append(domicilio)
            print("No existen posts")

    form = PublicacionesForm(None)
    if request.method == "POST":
        form = PublicacionesForm(request.POST, request.FILES)
        if form.is_valid():

            if request.POST['horario_desde'] == request.POST['horario_hasta']:
                messages.warning(request,
                                 'Ocurrió un error con los datos enviados. el horario de inicio y el horarioo final no pueden ser .',
                                 extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:propietarios_publicaciones'))

            else:

                data_post = Alquiler()

                data_post.tipo_post = request.POST['tipo_post']
                if 'categoria_post' in request.POST:
                    data_post.categoria_post = request.POST['categoria_post']
                else:
                    data_post.categoria_post = "VENTA"
                data_post.titulo = request.POST['titulo']
                data_post.descripcion = request.POST['descripcion']
                if 'imagen' in request.FILES:
                    data_post.imagen = request.FILES['imagen']
                else:
                    data_post.imagen = None
                data_post.cod_tlf = request.POST['cod_tlf']
                data_post.contacto = request.POST['contacto']
                data_post.horario_desde = request.POST['horario_desde']
                data_post.horario_hasta = request.POST['horario_hasta']
                data_post.is_active = True
                data_post.id_domicilio_id = request.POST['domicilio']

                data_post.save()

                # TODO: add message or redirect ?!
                messages.success(request,
                                 '¡La publicación fue realizada con exito!. El post ha sido publicado en la página.',
                                 extra_tags='alert-success')
                return HttpResponseRedirect(reverse('condominio_app:propietarios_publicaciones'))

        else:
            primera_key = next(iter(form.errors))
            messages.warning(request,
                             form.errors[primera_key].as_text().replace('*', ''),
                             extra_tags='alert-danger')

            return HttpResponseRedirect(reverse('condominio_app:propietarios_publicaciones'))

    return render(request, 'propietarios/propietarios_publicaciones.html', {'form': form, 'posts': posts, 'user': propietario,
                                                                            'domicilios': domicilios})


# A partir de aquí irán las vistas del modulo del administrador
# ------------------------------VISTAS ADMINISTRADOR------------------------------

def actualizar_tasa():
    response = ''
    count = 0
    while response == '':
        try:
            print("Conectando con 'https://www.bcv.org.ve/'")
            response = requests.get('https://www.bcv.org.ve/', verify=False)
            break
        except Exception as e:
            count += 1
            print(str(e))
            print("No se pudo conectar al BCV")
            print("Reintentando en 5 segundos")
            time.sleep(5)
            if count == 5:
                print("No se actualizó la tasa")
                break
            print("Reintentando...")
            continue

    if response != '':

        content = response.text
        soup = BeautifulSoup(content, 'lxml')

        box = soup.find('div', id='dolar')
        valor_dolar = round(float(box.find('strong').text.replace(',', '.')), 2)
        box = soup.find('div', id='euro')
        valor_euro = round(float(box.find('strong').text.replace(',', '.')), 2)
        texto_fecha = soup.find('span', class_='date-display-single').text
        fecha = date.today().strftime("%d/%m/%Y")
        print("D: ", valor_dolar)
        print("E: ", valor_euro)
        print(fecha)

        tasas = {'tasa_BCV_USD': valor_dolar,
                 'tasa_BCV_EUR': valor_euro}

        return tasas

    else:
        tasas = {'tasa_BCV_USD': 0,
                 'tasa_BCV_EUR': 0}
        return tasas


def comprobar_tasa(request, today, fecha_actual, dia_semana, tasa_bolivares, tasa_euros):
    if today != fecha_actual:
        print("Es un día diferente")
        if dia_semana == 'Monday' or 'Tuesday' or 'Wednesday' or 'Thursday' or 'Friday':
            print(dia_semana)
            tasas = actualizar_tasa()
            if tasas['tasa_BCV_USD'] != 0:
                tasa_bolivares = tasas['tasa_BCV_USD']
                tasa_euros = tasas['tasa_BCV_EUR']
                created = Tasas.objects.get_or_create(tasa_BCV_USD=tasa_bolivares,
                                                      tasa_BCV_EUR=tasa_euros,
                                                      created_at=datetime.now(),
                                                      updated_at=datetime.now())
                today = timezone.now()
                tasas = {'tasa_BCV_USD': tasa_bolivares,
                         'tasa_BCV_EUR': tasa_euros}
                return tasas
            else:
                messages.warning(request,
                                 '¡Debe establecer la tasa de cambio del día debido a que no se pudo conectar al BCV {}!'.format(
                                     today, extra_tags='alert-danger'))
                tasas = {'tasa_BCV_USD': tasa_bolivares,
                         'tasa_BCV_EUR': tasa_euros}
                return tasas
        elif dia_semana == 'Saturday' or 'Sunday':
            tasas = {'tasa_BCV_USD': tasa_bolivares,
                     'tasa_BCV_EUR': tasa_euros}
            return tasas
    else:
        print("mismo dia")
        tasas = {'tasa_BCV_USD': tasa_bolivares,
                 'tasa_BCV_EUR': tasa_euros}
        return tasas


@login_required
def home_admin(request):
    user = request.user
    try:
        usuario = Usuario.objects.get(pk=user.pk)
    except Usuario.DoesNotExist:
        return HttpResponseRedirect(reverse('condominio_app:home'))
    if usuario.id_condominio_id is None:
        tipo = _tipo_panel_usuario(user)
        if tipo == 'superuser':
            return HttpResponseRedirect(reverse('condominio_app:home_superuser'))
        if tipo == 'propietario':
            return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.filter(id_condominio=usuario.id_condominio_id)
    primer_login = False if condominio.exists() else True
    ultima_tasa = Tasas.objects.last()
    today = timezone.now()

    tasa_bs = {}
    tasa_euro = {}

    if ultima_tasa is not None:
        tasa_bs = ultima_tasa.tasa_BCV_USD
        tasa_euro = ultima_tasa.tasa_BCV_EUR

        tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                               today.strftime("%A"), tasa_bs, tasa_euro)

        tasa_bs = tasas['tasa_BCV_USD']
        tasa_euro = tasas['tasa_BCV_EUR']

    else:
        tasas = actualizar_tasa()

        if tasas['tasa_BCV_USD'] != 0:
            tasa_bs = tasas['tasa_BCV_USD']
            tasa_euro = tasas['tasa_BCV_EUR']
            created = Tasas.objects.get_or_create(tasa_BCV_USD=tasa_bs,
                                                  tasa_BCV_EUR=tasa_euro,
                                                  created_at=datetime.now(),
                                                  updated_at=datetime.now())
            today = timezone.now()
        else:
            messages.warning(request,
                             '¡Debe establecer la tasa de cambio del día debido a que no se pudo conectar al BCV {}!'.format(
                                 today, extra_tags='alert-danger'))
            tasa_bs = 0.00
            tasa_euro = 0.00

    return render(request, 'administrador/home.html', {'usuario': usuario, 'conf': condominio,
                                                       'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro, 'primer_login': primer_login})


@login_required
def admin_bancos(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    ultima_tasa = Tasas.objects.all().last()
    if not ultima_tasa:
        messages.warning(request, 'Configure las tasas de cambio en Configuración antes de usar este módulo.', extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': 'tasa'}))
    banks = Bancos.objects.all().values()
    bancos_form = BancosForm()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':

        print("xd")

        if request.POST['tipo_dni_titular'] == '':
            # Este error ocurre si no se ha escogido un tipo de dni
            messages.warning(request,
                             'Ha ocurrido un error durante el registro. Debe escoger un tipo de identificación',
                             extra_tags='alert-danger')
            print("xd0")
        else:

            print("xd2")

            bancos_form = BancosForm(data=request.POST, files=request.FILES)

            print("xd3")

            if bancos_form.is_valid():
                print("xd4")
                bancos = bancos_form.save()
                print("xd5")
                bancos.fecha_apertura = request.POST['fecha_apertura']
                bancos.saldo_apertura = request.POST['saldo_actual']
                bancos.id_condominio = condominio
                if request.FILES.get('imagen_referencial'):
                    bancos.imagen_referencial = request.FILES['imagen_referencial']
                bancos.save()
                print("xd6")

                messages.success(request, '¡El banco ha sido registrado de manera satisfactoria!',
                                 extra_tags='alert-success')
                return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "bancos"}))

            else:
                print("xderror")
                print(bancos_form.errors)
                messages.warning(request,
                                 'Ha ocurrido un error durante el registro. Por favor verifique e intente nuevamente',
                                 extra_tags='alert-danger')

    return render(request, 'administrador/bancos.html', {'bancos': banks, 'bancos_form': bancos_form,
                                                         'conf': condominio, 'tasa_bs': tasa_bs,
                                                         'tasa_euro': tasa_euro})


# ------------------------------ADMINISTRACION Y GESTION DE GASTOS------------------------------
@login_required
def admin_gastos(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    ultima_tasa = Tasas.objects.all().last()
    if not ultima_tasa:
        messages.warning(request, 'Configure las tasas de cambio en Configuración antes de usar este módulo.', extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': 'tasa'}))
    gastos = Gastos.objects.filter(
        id_movimiento__id_banco__id_condominio_id=user.id_condominio_id
    ).select_related("id_movimiento__id_banco")
    bancos = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
    propietarios = Domicilio.objects.filter(id_condominio_id=user.id_condominio_id).select_related('id_propietario')
    categorias = Categoria.objects.all()
    if not categorias.exists():
        Categoria.objects.create(nombre_categoria="General")
        categorias = Categoria.objects.all()
    cierre = Cierre_mes.objects.filter(id_condominio_id=user.id_condominio_id).order_by('fecha_cierre').last()
    if cierre:
        gastos = gastos.filter(id_movimiento__created_at__gt=cierre.fecha_cierre)
    gastos = gastos.order_by(
        '-id_movimiento__fecha_movimiento',
        '-id_movimiento__created_at',
        '-id_gasto'
    )
    cierre_fecha = cierre.fecha_cierre if cierre else None
    for gasto_item in gastos:
        if not cierre_fecha or not gasto_item.id_movimiento.created_at:
            gasto_item.can_modify = True
            continue
        gasto_item.can_modify = gasto_item.id_movimiento.created_at > cierre_fecha
    gasto = Gastos()
    movimiento = Movimientos_bancarios()
    deudas = Deudas()
    
    movimiento_form = MovimientoForm()
    datos_transaccion_form = DatosMovimientoForm()
    gastos_form = GastosForm()

    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        if request.POST['fecha_movimiento'] > str(date.today()):
            # Este error ocurre si la fecha escogida es mayor a la actual
            messages.warning(request,
                             'Ha ocurrido un error durante el registro. La fecha del gasto no puede ser mayor a la del día actual',
                             extra_tags='alert-danger')
        else:

            if Decimal(request.POST['monto_movimiento']) <= 0:
                messages.warning(request,
                                 'Ha ocurrido un error durante el registro. El monto del gasto no puede ser igual o menor a 0',
                                 extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_ingresos'))

            # La fecha es menor por lo que se prosigue con el registro de gastos
            id_bank = None
            if request.POST.get('banco_gasto_BS'):
                id_bank = Bancos.objects.get(id_banco=request.POST['banco_gasto_BS'])

            if request.POST.get('banco_gasto_USD'):
                id_bank = Bancos.objects.get(id_banco=request.POST['banco_gasto_USD'])

            if request.POST.get('banco_gasto_EUR'):
                id_bank = Bancos.objects.get(id_banco=request.POST['banco_gasto_EUR'])

            if not id_bank:
                messages.warning(request,
                                 'Debe seleccionar un banco para registrar el gasto.',
                                 extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_gastos'))

            monto = Decimal(request.POST['monto_movimiento'])

            if id_bank.saldo_actual < monto:
                messages.warning(request, '¡El banco no dispone de la cantidad ingresada para realizar el gasto!',
                                 extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_gastos'))

            dataBanco = {
                'concepto_movimiento': (request.POST.get('descripcion_movimiento') or '')[:255],
                'descripcion_movimiento': request.POST['descripcion_movimiento'],
                'referencia_movimiento': request.POST['referencia_movimiento'],
                'monto_movimiento': monto
            }

            movimiento_nuevo = MovimientoForm(data=dataBanco)

            if movimiento_nuevo.is_valid():

                mov_realizado = movimiento_nuevo.save()

                ult_movimiento = Movimientos_bancarios.objects.filter(id_banco_id=id_bank).last()

                mov_realizado.tipo_moneda = request.POST['TipoMonedaGasto'].upper()
                mov_realizado.id_banco = id_bank
                if ult_movimiento:
                    if ult_movimiento.debito_movimiento:
                        mov_realizado.debito_movimiento = ult_movimiento.debito_movimiento + monto
                    else:
                        mov_realizado.debito_movimiento = monto

                    if ult_movimiento.credito_movimiento:
                        mov_realizado.credito_movimiento = ult_movimiento.credito_movimiento
                    else:
                        mov_realizado.credito_movimiento = 0
                else:
                    mov_realizado.debito_movimiento = monto
                    mov_realizado.credito_movimiento = 0

                mov_realizado.save()

            else:
                print(movimiento_nuevo.errors)
                messages.warning(request,
                                 'Ha ocurrido un error durante el registro. Por favor verifique e intente nuevamente',
                                 extra_tags='alert-danger')

            if 'imgGasto' in request.FILES:
                gasto.imagen_referencial = request.FILES['imgGasto']
            else:
                gasto.imagen_referencial = None
            if request.POST['factura']:
                gasto.factura = request.POST['factura']
            else:
                gasto.factura = None

            gasto.concepto_movimiento = (request.POST.get('descripcion_movimiento') or '')[:255]
            gasto.fecha_movimiento = request.POST['fecha_movimiento']
            gasto.tipo_gasto = request.POST['tipo_gasto']
            gasto.metodo_pago = request.POST['metodo_pago']
            gasto.forma_cobro = request.POST['tipo_cobro_gasto']
            categoria_id = request.POST.get('categoria_gasto')
            if not categoria_id or categoria_id == '':
                categoria_default = Categoria.objects.first()
                if not categoria_default:
                    categoria_default = Categoria.objects.create(nombre_categoria="General")
                gasto.id_categoria_id = categoria_default.id_categoria
            else:
                gasto.id_categoria_id = categoria_id
            gasto.id_movimiento_id = mov_realizado.id_movimiento
            gasto.save()

            if request.POST.get('tipo_cobro_gasto') == 'Cuota':
                if request.POST['tipo_gasto'] == "COMÚN":
                    for prop in propietarios:
                        dom = Domicilio.objects.get(id_domicilio=prop.id_domicilio)

                        deudas.fecha_deuda = request.POST['fecha_movimiento']
                        deudas.concepto_deuda = (request.POST.get('descripcion_movimiento') or '')[:255]
                        deudas.descripcion = request.POST['descripcion_movimiento'].upper()
                        deudas.tipo_deuda = 1
                        deudas.categoria_deuda = "CUOTA EXTRA"
                        deudas.monto_deuda = monto
                        deudas.is_active = True
                        deudas.created_at = today
                        deudas.updated_at = today
                        deudas.id_domicilio = dom
                        deudas.is_moroso = False

                        dom.estado_deuda = True

                        dom.save()
                        deudas.save()
                else:
                    prop_individual = Domicilio.objects.get(id_domicilio=request.POST['prop_selected'])

                    deudas.fecha_deuda = request.POST['fecha_movimiento']
                    deudas.concepto_deuda = (request.POST.get('descripcion_movimiento') or '')[:255]
                    deudas.descripcion = request.POST['descripcion_gasto'].upper()
                    deudas.tipo_deuda = 1
                    deudas.categoria_deuda = "CUOTA EXTRA"
                    deudas.monto_deuda = monto
                    deudas.is_active = True
                    deudas.created_at = today
                    deudas.updated_at = today
                    deudas.id_domicilio = prop_individual
                    deudas.is_moroso = False

                    prop_individual.estado_deuda = True

                    prop_individual.save()
                    deudas.save()

            data_mov = Datos_transaccion()

            data_mov.nombre_titular = request.POST['nombre_titular']
            data_mov.codigo_area = request.POST['codigo_area']
            data_mov.telefono_titular = request.POST['telefono_titular']
            data_mov.dni_titular = request.POST['tipo_dni_titular'] + "-" + request.POST['dni_titular']
            data_mov.tipo_transaccion = "GASTO"
            data_mov.id_movimiento_id = mov_realizado.id_movimiento
            data_mov.save()

            Bancos.objects.filter(pk=id_bank.id_banco).update(saldo_anterior=id_bank.saldo_actual,
                                                              saldo_actual=id_bank.saldo_actual - monto,
                                                              debitos_banco=id_bank.debitos_banco + monto,
                                                              ultimo_debito=timezone.now())

            tasa_USD = Decimal(tasa_bs)
            tasa_EUR = Decimal(tasa_euro)

            if id_bank.tipo_moneda == 'BS':
                condominio.saldo_edificio -= monto
            elif id_bank.tipo_moneda == 'USD':
                usd_cambio = tasa_USD * monto
                condominio.saldo_edificio_usd -= usd_cambio
            elif id_bank.tipo_moneda == 'EUR':
                eur_cambio = tasa_EUR * monto
                condominio.saldo_edificio_eur -= eur_cambio

            messages.success(request, '¡El gasto ha sido registrado de manera satisfactoria!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_gastos').rstrip('/') + '?lista=1')

    return render(request, 'administrador/gastos.html', {'gastos': gastos, 'bancos': bancos,
                                                         'gastos_form': gastos_form, 'movimiento_form': movimiento_form,
                                                         'datos_transaccion_form': datos_transaccion_form,
                                                         'conf': condominio, 'propietarios': propietarios,
                                                         'categorias': categorias, 'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro,
                                                         'cierre': cierre})


# ------------------------------ADMINISTRACION Y GESTION DE INGRESOS------------------------------
@login_required
def admin_ingresos(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    ultima_tasa = Tasas.objects.all().last()
    if not ultima_tasa:
        messages.warning(request, 'Configure las tasas de cambio en Configuración antes de usar este módulo.', extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': 'tasa'}))
    ingresos = Ingresos.objects.filter(
        id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        id_movimiento__estado_movimiento=0,
    ).select_related("id_movimiento__id_banco")
    cierre = Cierre_mes.objects.filter(id_condominio_id=user.id_condominio_id).last()
    if cierre:
        ingresos = ingresos.filter(id_movimiento__created_at__gt=cierre.fecha_cierre)
    ingresos = ingresos.order_by(
        '-id_movimiento__fecha_movimiento',
        '-id_movimiento__created_at',
        '-id_ingreso'
    )
    for ingreso in ingresos:
        ingreso.emisor = ""
        if ingreso.id_propietario:
            ingreso.emisor = ingreso.id_propietario.nombre_propietario
        else:
            recibo = Recibos.objects.filter(id_movimiento_id=ingreso.id_movimiento_id).select_related('id_deuda__id_domicilio__id_propietario').first()
            if recibo and recibo.id_deuda and recibo.id_deuda.id_domicilio and recibo.id_deuda.id_domicilio.id_propietario:
                ingreso.emisor = recibo.id_deuda.id_domicilio.id_propietario.nombre_propietario
            if not ingreso.emisor:
                datos_transaccion = Datos_transaccion.objects.filter(id_movimiento_id=ingreso.id_movimiento_id).first()
                if datos_transaccion and datos_transaccion.nombre_titular:
                    ingreso.emisor = datos_transaccion.nombre_titular
        if ingreso.id_movimiento.estado_movimiento == 2:
            ingreso.estado_label = "Pendiente"
            ingreso.estado_bloqueado = False
        elif ingreso.id_movimiento.estado_movimiento == 1:
            ingreso.estado_label = "Rechazado"
            ingreso.estado_bloqueado = True
        else:
            if cierre and ingreso.id_movimiento.created_at and ingreso.id_movimiento.created_at < cierre.fecha_cierre:
                ingreso.estado_label = "Cerrado"
                ingreso.estado_bloqueado = True
            else:
                ingreso.estado_label = "Pagada"
                ingreso.estado_bloqueado = False
    bancos = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
    propietarios = Domicilio.objects.filter(id_condominio_id=user.id_condominio_id).select_related('id_propietario')
    # cierre ya calculado arriba para el condominio
    
    ingreso = Ingresos()
    movimiento = Movimientos_bancarios()
    
    movimiento_form = MovimientoForm()
    datos_transaccion_form = DatosMovimientoForm()
    ingresos_form = IngresosForm()
    
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        if request.POST['fecha_movimiento'] > str(date.today()):
            # Este error ocurre si la fecha escogida es mayor a la actual
            messages.warning(request,
                             'Ha ocurrido un error durante el registro. La fecha del ingreso no puede ser mayor a la del día actual',
                             extra_tags='alert-danger')
        else:

            # La fecha es menor y se continua con el registro de ingresos
            if Decimal(request.POST['monto_movimiento']) <= 0:
                messages.warning(request,
                                 'Ha ocurrido un error durante el registro. El monto del ingreso no puede ser igual o menor a 0',
                                 extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_ingresos'))

            if 'banco_ingreso_BS' in request.POST:
                id_bank = Bancos.objects.get(id_banco=request.POST['banco_ingreso_BS'])

            if 'banco_ingreso_USD' in request.POST:
                id_bank = Bancos.objects.get(id_banco=request.POST['banco_ingreso_USD'])

            if 'banco_ingreso_EUR' in request.POST:
                id_bank = Bancos.objects.get(id_banco=request.POST['banco_ingreso_EUR'])

            try:
                id_owner = Domicilio.objects.get(id_domicilio=request.POST['apto_ingreso'])
            except:
                id_owner = None

            monto = Decimal(request.POST['monto_movimiento'])

            dataBanco = {
                'concepto_movimiento': (request.POST.get('descripcion_movimiento') or '')[:255],
                'descripcion_movimiento': request.POST['descripcion_movimiento'],
                'referencia_movimiento': request.POST['referencia_movimiento'],
                'monto_movimiento': monto
            }

            movimiento_nuevo = MovimientoForm(data=dataBanco)

            if movimiento_nuevo.is_valid():

                mov_realizado = movimiento_nuevo.save()

                ult_movimiento = Movimientos_bancarios.objects.filter(id_banco_id=id_bank).last()

                mov_realizado.tipo_moneda = request.POST['TipoMonedaIngreso'].upper()
                mov_realizado.id_banco = id_bank
                mov_realizado.estado_movimiento = 0
                if ult_movimiento:
                    if ult_movimiento.debito_movimiento:
                        mov_realizado.debito_movimiento = ult_movimiento.debito_movimiento
                    else:
                        mov_realizado.debito_movimiento = 0

                    if ult_movimiento.credito_movimiento:
                        mov_realizado.credito_movimiento = ult_movimiento.credito_movimiento + monto
                    else:
                        mov_realizado.credito_movimiento = monto
                else:
                    mov_realizado.debito_movimiento = 0
                    mov_realizado.credito_movimiento = monto

                mov_realizado.save()

            else:
                print(movimiento_nuevo.errors)
                messages.warning(request,
                                 'Ha ocurrido un error durante el registro. Por favor verifique e intente nuevamente',
                                 extra_tags='alert-danger')

            if 'imgIngreso' in request.FILES:
                ingreso.imagen_referencial = request.FILES['imgIngreso']
            else:
                ingreso.imagen_referencial = None

            if request.POST['factura']:
                ingreso.factura = request.POST['factura']
            else:
                ingreso.factura = None

            ingreso.concepto_movimiento = (request.POST.get('descripcion_movimiento') or '')[:255]
            ingreso.tipo_ingreso = request.POST['tipo_ingreso']
            ingreso.metodo_pago = request.POST['metodo_pago']
            ingreso.id_movimiento_id = mov_realizado.id_movimiento
            if id_owner is not None and id_owner.id_propietario_id:
                ingreso.id_propietario = id_owner.id_propietario
            ingreso.save()

            data_mov = Datos_transaccion()

            data_mov.nombre_titular = request.POST['nombre_titular']
            data_mov.codigo_area = request.POST['codigo_area']
            data_mov.telefono_titular = request.POST['telefono_titular']
            data_mov.dni_titular = request.POST['tipo_dni_titular'] + "-" + request.POST['dni_titular']
            data_mov.tipo_transaccion = "INGRESO"
            data_mov.id_movimiento_id = mov_realizado.id_movimiento
            data_mov.save()

            Bancos.objects.filter(pk=id_bank.id_banco).update(saldo_anterior=id_bank.saldo_actual,
                                                              saldo_actual=id_bank.saldo_actual + monto,
                                                              creditos_banco=id_bank.creditos_banco + monto,
                                                              ultimo_credito=timezone.now())

            tasa_USD = Decimal(tasa_bs)
            tasa_EUR = Decimal(tasa_euro)

            if id_bank.tipo_moneda == 'BS':
                condominio.saldo_edificio += monto

            elif id_bank.tipo_moneda == 'USD':
                usd_cambio = tasa_USD * monto
                condominio.saldo_edificio_usd += usd_cambio

            elif id_bank.tipo_moneda == 'EUR':
                eur_cambio = tasa_EUR * monto
                condominio.saldo_edificio_eur += eur_cambio

            # Si se eligió apartamento: acreditar el monto al saldo del inmueble en la moneda seleccionada
            if id_owner is not None:
                if id_bank.tipo_moneda == 'BS':
                    id_owner.saldo = (id_owner.saldo or Decimal('0')) + monto
                    id_owner.save(update_fields=['saldo'])
                elif id_bank.tipo_moneda == 'USD':
                    id_owner.saldo_usd = (id_owner.saldo_usd or Decimal('0')) + monto
                    id_owner.save(update_fields=['saldo_usd'])
                elif id_bank.tipo_moneda == 'EUR':
                    id_owner.saldo_eur = (id_owner.saldo_eur or Decimal('0')) + monto
                    id_owner.save(update_fields=['saldo_eur'])

            messages.success(request, '¡El ingreso ha sido registrado de manera satisfactoria!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_ingresos'))

    return render(request, 'administrador/ingresos.html', {'ingresos': ingresos, 'bancos': bancos,
                                                           'ingresos_form': ingresos_form, 'propietarios': propietarios,
                                                           'conf': condominio, 'tasa_bs': tasa_bs,
                                                           'movimiento_form': movimiento_form,
                                                           'datos_transaccion_form': datos_transaccion_form,
                                                           'tasa_euro': tasa_euro, 'cierre': cierre})

# ------------------------------ADMINISTRACION Y GESTION DE DEUDAS------------------------------
@login_required
def admin_deudas(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    gastos = Gastos.objects.all()
    cierre = Cierre_mes.objects.filter(id_condominio_id=user.id_condominio_id).order_by('fecha_cierre').last()
    deudas_prop = Deudas.objects.filter(
        is_active=True,
        id_domicilio__estado_deuda=True,
        tipo_deuda="2",
        id_domicilio__id_condominio_id=user.id_condominio_id,
    ).order_by('id_domicilio__id_propietario_id').distinct('id_domicilio__id_propietario_id')
    deudas_condo = Deudas.objects.filter(
        is_active=True,
        tipo_deuda="1",
        id_domicilio__id_condominio_id=user.id_condominio_id,
    )
    # Propietarios con al menos un inmueble en el condominio O con usuario en el condominio
    propietarios = Propietario.objects.filter(
        Q(prop_dom__id_condominio_id=user.id_condominio_id) | Q(id_usuario__id_condominio_id=user.id_condominio_id)
    ).distinct()
    totales_deudas = Deudas.objects.filter(
        is_active=True,
        tipo_deuda="2",
        id_domicilio__id_condominio_id=user.id_condominio_id,
    ).values('tipo_moneda').annotate(total=Sum('monto_deuda'))
    total_deudas_bs = 0
    total_deudas_usd = 0
    total_deudas_eur = 0
    for item in totales_deudas:
        if item['tipo_moneda'] == 'BS':
            total_deudas_bs = item['total'] or 0
        elif item['tipo_moneda'] == 'USD':
            total_deudas_usd = item['total'] or 0
        elif item['tipo_moneda'] == 'EUR':
            total_deudas_eur = item['total'] or 0
    for deuda_item in deudas_prop:
        if not deuda_item.is_active:
            deuda_item.estado_label = "Pagada"
        elif cierre and deuda_item.created_at and deuda_item.created_at < cierre.fecha_cierre:
            deuda_item.estado_label = "Cerrado"
        else:
            deuda_item.estado_label = "Pendiente"

    deudas_form = DeudasForm()
    deuda = Deudas()
    ultima_tasa = Tasas.objects.last()
    if not ultima_tasa:
        messages.warning(request, 'Configure las tasas de cambio en Configuración antes de usar este módulo.', extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': 'tasa'}))
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        if request.POST['fecha_deuda'] > str(date.today()):
            # Este error ocurre si la fecha escogida es mayor a la actual
            messages.warning(request,
                             'Ha ocurrido un error durante el registro. La fecha de la deuda no puede ser mayor a la del día actual',
                             extra_tags='alert-danger')
        else:
            if float(request.POST['monto_deuda']) < 0:
                messages.warning(request, 'El monto no puede ser menor a 0.', extra_tags='alert-danger')
            else:
                if request.POST['tipo_deuda'] == "2":
                    propietario_id = request.POST.get('propietario_deudor')
                    domicilios_ids = request.POST.getlist('domicilios_deudor')

                    if not propietario_id or not domicilios_ids:
                        messages.warning(request,
                                         'Debe seleccionar un propietario y al menos un inmueble.',
                                         extra_tags='alert-danger')
                        return HttpResponseRedirect(reverse('condominio_app:admin_deudas'))

                    domicilios = Domicilio.objects.filter(
                        id_domicilio__in=domicilios_ids,
                        id_propietario_id=propietario_id,
                        id_condominio_id=user.id_condominio_id
                    )

                    if not domicilios:
                        messages.warning(request,
                                         'No se encontraron inmuebles válidos para el propietario seleccionado.',
                                         extra_tags='alert-danger')
                        return HttpResponseRedirect(reverse('condominio_app:admin_deudas'))

                    descripcion = request.POST.get('descripcion_deuda') or ''
                    concepto = (descripcion or request.POST.get('concepto_deuda') or '')[:255]
                    for domicilio in domicilios:
                        deuda = Deudas()
                        deuda.fecha_deuda = request.POST['fecha_deuda']
                        deuda.concepto_deuda = concepto
                        deuda.descripcion_deuda = descripcion
                        deuda.tipo_deuda = request.POST['tipo_deuda']
                        deuda.categoria_deuda = "CUOTA EXTRA"
                        deuda.monto_deuda = request.POST['monto_deuda']
                        deuda.tipo_moneda = request.POST['tipo_moneda']
                        deuda.is_active = True
                        deuda.created_at = today
                        deuda.updated_at = today
                        deuda.id_domicilio = domicilio
                        deuda.is_moroso = False

                        Domicilio.objects.filter(id_domicilio=domicilio.id_domicilio).update(estado_deuda=True)

                        deuda.save()

                    # No descontar saldo al crear la deuda. El descuento solo ocurre
                    # cuando el usuario elige "Descontar del saldo".

                else:
                    descripcion = request.POST.get('descripcion_deuda') or ''
                    deuda.tipo_deuda = request.POST['tipo_deuda']
                    deuda.is_moroso = False
                    deuda.concepto_deuda = (descripcion or request.POST.get('concepto_deuda') or '')[:255]
                    deuda.descripcion_deuda = descripcion
                    deuda.monto_deuda = request.POST['monto_deuda']
                    deuda.tipo_moneda = request.POST['tipo_moneda']
                    deuda.fecha_deuda = request.POST['fecha_deuda']
                    deuda.is_active = True
                    deuda.created_at = today
                    deuda.updated_at = today

                    deuda.save()

                messages.warning(request, '¡La deuda fue registada con exito!',
                                 extra_tags='alert-success')

        return HttpResponseRedirect(reverse('condominio_app:admin_deudas'))

    return render(request, 'administrador/deudas.html', {'conf': condominio, 'tasa_bs': tasa_bs,
                                                         'tasa_euro': tasa_euro, 'gastos': gastos, 'deudas_prop': deudas_prop,
                                                         'deudas_condo': deudas_condo, 'propietarios': propietarios,
                                                         'deudas_form': deudas_form,
                                                         'total_deudas_bs': total_deudas_bs,
                                                         'total_deudas_usd': total_deudas_usd,
                                                         'total_deudas_eur': total_deudas_eur})


@login_required
def admin_deudas_caja(request):
    user = request.user
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    # Propietarios con al menos un inmueble en el condominio O con usuario en el condominio
    propietarios = Propietario.objects.filter(
        Q(prop_dom__id_condominio_id=user.id_condominio_id) | Q(id_usuario__id_condominio_id=user.id_condominio_id)
    ).distinct()
    deudas_form = DeudasForm()
    ultima_tasa = Tasas.objects.last()
    today = timezone.now()

    tasa_bs = 0
    tasa_euro = 0
    if ultima_tasa:
        tasa_bs = ultima_tasa.tasa_BCV_USD
        tasa_euro = ultima_tasa.tasa_BCV_EUR
        tasas = comprobar_tasa(
            request,
            today.strftime("%d/%m/%Y"),
            ultima_tasa.updated_at.strftime("%d/%m/%Y"),
            today.strftime("%A"),
            tasa_bs,
            tasa_euro,
        )
        tasa_bs = tasas['tasa_BCV_USD']
        tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        try:
            fecha_pago = request.POST.get('fecha_movimiento', '')
            if fecha_pago and fecha_pago > str(date.today()):
                messages.warning(
                    request,
                    'La fecha del pago no puede ser mayor a la fecha actual.',
                    extra_tags='alert-danger',
                )
                return HttpResponseRedirect(reverse('condominio_app:admin_deudas_caja'))

            moneda_form = (request.POST.get('tipo_moneda') or request.POST.get('moneda_pago') or '').upper()
            moneda_pago = (request.POST.get('moneda_pago') or '').upper()
            if moneda_form != moneda_pago:
                messages.warning(
                    request,
                    'La moneda del pago no coincide con la moneda seleccionada.',
                    extra_tags='alert-danger',
                )
                return HttpResponseRedirect(reverse('condominio_app:admin_deudas_caja'))

            propietario_id = request.POST.get('propietario_pago')
            if not propietario_id:
                messages.warning(request, 'Debe seleccionar un propietario.', extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_deudas_caja'))

            deudas_ids = request.POST.getlist('montos_deudas')
            if not deudas_ids:
                messages.warning(request, 'Debe seleccionar al menos una deuda.', extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_deudas_caja'))

            deudas_qs = Deudas.objects.filter(
                id_deuda__in=deudas_ids,
                is_active=True,
                tipo_deuda=Deudas.TipoDeuda.PROPIETARIO,
                tipo_moneda=moneda_pago,
                id_domicilio__id_propietario_id=propietario_id,
                id_domicilio__id_condominio_id=user.id_condominio_id,
            ).select_related('id_domicilio')

            if deudas_qs.count() != len(deudas_ids):
                messages.warning(
                    request,
                    'Las deudas seleccionadas no son validas para el propietario o moneda indicada.',
                    extra_tags='alert-danger',
                )
                return HttpResponseRedirect(reverse('condominio_app:admin_deudas_caja'))

            total_deuda = deudas_qs.aggregate(total=Sum('monto_deuda'))['total'] or Decimal('0')
            monto_movimiento = Decimal(request.POST.get('monto_movimiento', '0'))
            if monto_movimiento <= 0:
                messages.warning(request, 'El monto debe ser mayor a 0.', extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_deudas_caja'))

            if monto_movimiento.quantize(Decimal('0.01')) != total_deuda.quantize(Decimal('0.01')):
                messages.warning(
                    request,
                    'El monto enviado no coincide con la suma de las deudas seleccionadas.',
                    extra_tags='alert-danger',
                )
                return HttpResponseRedirect(reverse('condominio_app:admin_deudas_caja'))

            banco = Bancos.objects.filter(
                id_condominio_id=user.id_condominio_id,
                tipo_moneda__iexact=moneda_pago,
            ).order_by('id_banco').first()
            if not banco:
                messages.warning(
                    request,
                    'No existe un banco configurado para la moneda seleccionada.',
                    extra_tags='alert-danger',
                )
                return HttpResponseRedirect(reverse('condominio_app:admin_deudas_caja'))

            ultimo_movimiento = Movimientos_bancarios.objects.filter(id_banco_id=banco.id_banco).order_by('id_movimiento').last()
            debito_acumulado = ultimo_movimiento.debito_movimiento if (ultimo_movimiento and ultimo_movimiento.debito_movimiento) else Decimal('0')
            credito_acumulado = ultimo_movimiento.credito_movimiento if (ultimo_movimiento and ultimo_movimiento.credito_movimiento) else Decimal('0')

            movimiento = Movimientos_bancarios.objects.create(
                concepto_movimiento=(request.POST.get('descripcion_movimiento') or 'PAGO DE DEUDAS')[:255],
                descripcion_movimiento='PAGO DE DEUDAS EN CAJA',
                referencia_movimiento=f"CAJA-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                monto_movimiento=monto_movimiento,
                debito_movimiento=debito_acumulado,
                credito_movimiento=credito_acumulado + monto_movimiento,
                estado_movimiento=0,
                tipo_moneda=moneda_pago,
                id_banco=banco,
                banco_emisor=request.POST.get('nombre_banco', ''),
            )

            ingreso = Ingresos(
                tipo_ingreso='PAGO DE DEUDA',
                metodo_pago=2,
                id_movimiento=movimiento,
            )
            if 'imgIngreso' in request.FILES:
                ingreso.imagen_referencial = request.FILES['imgIngreso']
            ingreso.save()

            Datos_transaccion.objects.create(
                nombre_titular=request.POST.get('nombre_titular', ''),
                nombre_banco=request.POST.get('nombre_banco', ''),
                tipo_transaccion='INGRESO',
                dni_titular=(request.POST.get('tipo_dni_titular', '') + "-" + request.POST.get('dni_titular', '')).strip('-'),
                id_movimiento=movimiento,
            )

            Bancos.objects.filter(pk=banco.id_banco).update(
                saldo_anterior=banco.saldo_actual,
                saldo_actual=(banco.saldo_actual or Decimal('0')) + monto_movimiento,
                creditos_banco=(banco.creditos_banco or Decimal('0')) + monto_movimiento,
                ultimo_credito=timezone.now(),
            )

            deudas_listado = list(deudas_qs)
            for deuda in deudas_listado:
                Recibos.objects.create(
                    descripcion_recibo=f"Pago deuda {deuda.concepto_deuda or deuda.id_deuda}",
                    monto=deuda.monto_deuda,
                    fecha_creacion=date.today(),
                    hora_creacion=timezone.now().time(),
                    categoria_recibo='SOLVENTE',
                    id_movimiento=movimiento,
                    id_deuda=deuda,
                )
                deuda.is_active = False
                deuda.save(update_fields=['is_active', 'updated_at'])

            domicilios_afectados = {deuda.id_domicilio_id for deuda in deudas_listado if deuda.id_domicilio_id}
            for domicilio_id in domicilios_afectados:
                tiene_deuda_activa = Deudas.objects.filter(id_domicilio_id=domicilio_id, is_active=True).exists()
                Domicilio.objects.filter(id_domicilio=domicilio_id).update(estado_deuda=tiene_deuda_activa)

            messages.success(request, 'Pago registrado y reflejado en ingresos correctamente.', extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_deudas_caja'))
        except Exception:
            messages.warning(
                request,
                'Ocurrio un error al registrar el pago en caja. Verifique los datos e intente nuevamente.',
                extra_tags='alert-danger',
            )
            return HttpResponseRedirect(reverse('condominio_app:admin_deudas_caja'))

    return render(
        request,
        'administrador/deudas_caja.html',
        {
            'conf': condominio,
            'tasa_bs': tasa_bs,
            'tasa_euro': tasa_euro,
            'deudas_form': deudas_form,
            'propietarios': propietarios,
        },
    )


# envia los datos al modal
def deudas_list(request):

    print(request.GET.get('id'))
    domicilios = Domicilio.objects.filter(id_propietario_id=request.GET.get('id'))
    
    deudas=[]
    for domicilio in domicilios:
        deudas_domicilio = Deudas.objects.filter(id_domicilio_id=domicilio.id_domicilio, is_active=True).select_related('id_domicilio')
        for deuda in deudas_domicilio:
            moroso = "Si" if deuda.is_active else "No"

            data_deuda = {
                'id_deuda': deuda.id_deuda,
                'concepto_deuda': deuda.concepto_deuda,
                'descripcion_deuda': deuda.descripcion_deuda,
                'monto_deuda': deuda.monto_deuda,
                'fecha_deuda': deuda.fecha_deuda,
                'is_moroso': moroso,
                'domicilio': domicilio.nombre_domicilio,
                'categoria_deuda': deuda.categoria_deuda,
                'tipo_moneda': deuda.tipo_moneda,

            }
            deudas.append(data_deuda)

    lista = {
        'deudas': deudas
    }

    return JsonResponse(lista)


@login_required       
def recibo_total_deuda(request, id):
    user = request.user
    propietarios = Propietario.objects.get(id_propietario=id)
    data = Deudas.objects.all().select_related('id_domicilio')
    domicilios = Domicilio.objects.filter(id_propietario_id=id)
    
    deudas=[] 
    for domicilio in domicilios: 
        deudas_domicilio = Deudas.objects.filter(id_domicilio_id=domicilio.id_domicilio, is_active=True).select_related('id_domicilio')
        for deuda in deudas_domicilio:
            deudas.append(deuda)
            
    print(deudas)
    for deuda in deudas:
        print(deuda.id_domicilio.nombre_domicilio)
        
    name_pdf = 'Lista de deudas' + '.pdf'

    ruta_logo = os.path.join(os.getcwd(), 'static', 'img-inverdata', 'logo_inverdata_pdf.png')

    condominio = get_object_or_404(Condominio, id_condominio=propietarios.id_usuario.id_condominio_id)
    todos_bancos = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
    nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
    html_string = render_to_string('PDF/deudas_propietarios.html', {
        'deudas': deudas,
        'datos_condominio': condominio,
        'bancos_cabecera': [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in todos_bancos],
        'fecha_generado': timezone.now(),
    })
   # Crear un objeto HTML a partir de la cadena HTML
    # html = HTML(string=html_string, base_url=request.build_absolute_uri())  # DESACTIVADO - Windows GTK
    # css = CSS(filename='static/css/bootstrap.min.css')  # DESACTIVADO - Windows GTK
    # pdf_file = html.write_pdf()  # DESACTIVADO - Windows GTK
    
    # Generar el archivo PDF usando xhtml2pdf (pisa)
    result = io.BytesIO()
    pisa.CreatePDF(html_string, dest=result, link_callback=link_callback)
    pdf_file = result.getvalue()

    # Devolver el archivo PDF como respuesta
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="' + name_pdf + '"'
    response.write(pdf_file)
    return response

# ------------------------------ADMINISTRACION Y GESTION DE FONDOS------------------------------
@login_required
def admin_fondos(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    bancos = Bancos.objects.filter(id_condominio_id=condominio.id_condominio, tipo_banco="FONDO")
    fondos = Fondos.objects.filter(id_movimiento__id_banco__id_condominio_id=user.id_condominio_id).select_related("id_movimiento__id_banco")
    
    fondo = Fondos()
    movimiento = Movimientos_bancarios()

    fondos_form = FondosForm()
    movimiento_form = MovimientoForm()
    datos_transaccion_form = DatosMovimientoForm()

    ultima_tasa = Tasas.objects.all().last()
    if not ultima_tasa:
        messages.warning(request, 'Configure las tasas de cambio en Configuración antes de usar este módulo.', extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': 'tasa'}))
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        if request.POST['fecha_movimiento'] > str(date.today()):
            # Este error ocurre si la fecha escogida es mayor a la actual
            messages.warning(request,
                             'Ha ocurrido un error durante el registro. La fecha del fondo no puede ser mayor a la del día actual',
                             extra_tags='alert-danger')
        else:

            # La fecha es menor y se continua con el registro de ingresos
            if Decimal(request.POST['monto_movimiento']) <= 0:
                messages.warning(request,
                                 'Ha ocurrido un error durante el registro. El monto del fondo no puede ser igual o menor a 0',
                                 extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_ingresos'))

            if 'banco_BS' in request.POST:
                id_bank = Bancos.objects.get(id_banco=request.POST['banco_BS'])

            if 'banco_USD' in request.POST:
                id_bank = Bancos.objects.get(id_banco=request.POST['banco_USD'])

            if 'banco_EUR' in request.POST:
                id_bank = Bancos.objects.get(id_banco=request.POST['banco_EUR'])

            try:
                id_owner = Domicilio.objects.get(id_domicilio=request.POST['apto_ingreso'])
            except:
                id_owner = None

            monto = Decimal(request.POST['monto_movimiento'])

            dataBanco = {
                'concepto_movimiento': (request.POST.get('descripcion_movimiento') or '')[:255],
                'descripcion_movimiento': request.POST['descripcion_movimiento'],
                'referencia_movimiento': request.POST['referencia_movimiento'],
                'monto_movimiento': monto
            }

            movimiento_nuevo = MovimientoForm(data=dataBanco)

            if movimiento_nuevo.is_valid():

                mov_realizado = movimiento_nuevo.save()

                ult_movimiento = Movimientos_bancarios.objects.filter(id_banco_id=id_bank).last()

                mov_realizado.tipo_moneda = request.POST['TipoMoneda']
                mov_realizado.id_banco = id_bank
                if ult_movimiento:
                    if ult_movimiento.debito_movimiento:
                        mov_realizado.debito_movimiento = ult_movimiento.debito_movimiento
                    else:
                        mov_realizado.debito_movimiento = 0

                    if ult_movimiento.credito_movimiento:
                        mov_realizado.credito_movimiento = ult_movimiento.credito_movimiento + monto
                    else:
                        mov_realizado.credito_movimiento = monto
                else:
                    mov_realizado.debito_movimiento = 0
                    mov_realizado.credito_movimiento = monto

                mov_realizado.save()

            else:
                print(movimiento_nuevo.errors)
                messages.warning(request,
                                 'Ha ocurrido un error durante el registro. Por favor verifique e intente nuevamente',
                                 extra_tags='alert-danger')

            if 'imgFondo' in request.FILES:
                fondo.imagen_referencial = request.FILES['imgFondo']
            else:
                fondo.imagen_referencial = None

            if request.POST['factura']:
                fondo.factura = request.POST['factura']
            else:
                fondo.factura = None

            fondo.concepto_movimiento = (request.POST.get('descripcion_movimiento') or '')[:255]
            fondo.tipo_fondo = request.POST['tipo_fondo']
            fondo.metodo_pago = request.POST['metodo_pago']
            fondo.id_movimiento_id = mov_realizado.id_movimiento
            fondo.save()

            data_mov = Datos_transaccion()

            data_mov.nombre_titular = request.POST['nombre_titular']
            data_mov.codigo_area = request.POST['codigo_area']
            data_mov.telefono_titular = request.POST['telefono_titular']
            data_mov.dni_titular = request.POST['tipo_dni_titular'] + "-" + request.POST['dni_titular']
            data_mov.tipo_transaccion = "FONDO"
            data_mov.id_movimiento_id = mov_realizado.id_movimiento
            data_mov.save()

            Bancos.objects.filter(pk=id_bank.id_banco).update(saldo_anterior=id_bank.saldo_actual,
                                                              saldo_actual=id_bank.saldo_actual + monto,
                                                              creditos_banco=id_bank.creditos_banco + monto,
                                                              ultimo_credito=timezone.now())

            tasa_USD = Decimal(tasa_bs)
            tasa_EUR = Decimal(tasa_euro)

            if id_bank.tipo_moneda == 'BS':
                condominio.saldo_edificio += monto

            elif id_bank.tipo_moneda == 'USD':
                usd_cambio = tasa_USD * monto
                condominio.saldo_edificio_usd += usd_cambio

            elif id_bank.tipo_moneda == 'EUR':
                eur_cambio = tasa_EUR * monto
                condominio.saldo_edificio_eur += eur_cambio

            messages.success(request, '¡El fondo ha sido registrado de manera satisfactoria!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_fondos'))

    return render(request, 'administrador/fondos.html', {'conf': condominio, 'tasa_bs': tasa_bs,
                                                         'tasa_euro': tasa_euro, 'fondos_form': fondos_form,
                                                         'movimiento_form': movimiento_form,
                                                         'datos_transaccion_form': datos_transaccion_form,
                                                         'bancos': bancos, 'fondos': fondos})

def procesar_propietario_post(request):
    # tipo_dni debe venir del POST (valor del select: V, E, P, J, G, R, O); si no, no usar default
    tipo_dni_raw = (request.POST.get('tipo_dni') or '').strip()
    if not tipo_dni_raw:
        messages.warning(request,
                         'Debe escoger un tipo de documento (Venezolano, RIF, Jurídico, etc.).',
                         extra_tags='alert-danger')
        return False

    dataPropietario = {
        'nombre_propietario': request.POST.get('nombre_propietario', '').upper(),
        'genero': request.POST.get('genero'),
        'pais_residencia': request.POST.get('pais_residencia'),
        'tipo_dni': tipo_dni_raw,
        'dni': request.POST.get('dni'),
        'codigo_tlf_hab': request.POST.get('codigo_tlf_hab'),
        'telefono_hab': request.POST.get('telefono_hab'),
        'codigo_tlf_movil': request.POST.get('codigo_tlf_movil'),
        'telefono_movil': request.POST.get('telefono_movil'),
        'correo': request.POST.get('email'),
        'condominio': request.user.id_condominio_id
    }

    dataUsuario = {
        'username': dataPropietario['dni'],
        'email': request.POST.get('email'),
        'password1': dataPropietario['dni']
    }

    if Usuario.objects.filter(email=dataUsuario['email']).exists():
        messages.warning(request,
                         'Ha ocurrido un error durante el registro. El correo ya está registrado.',
                         extra_tags='alert-danger')
        return False

    propietarios_form = PropietariosForm(data=dataPropietario)
    if propietarios_form.is_valid():
        prop = propietarios_form.save()

        aptos = ""
        for i, domicilios in enumerate(request.POST.getlist('domicilio')):
            dom_seleccionados = Domicilio.objects.get(id_domicilio=int(domicilios))
            dom_seleccionados.id_propietario = prop
            dom_seleccionados.save()
            if i == 0:
                aptos = dom_seleccionados.nombre_domicilio
            else:
                aptos = aptos + ', ' + dom_seleccionados.nombre_domicilio

        usuario = RegistrationForm(data=dataUsuario)
        if usuario.is_valid():
            acc = usuario.save(commit=False)
            acc.set_password(dataPropietario['dni'])
            rol_propietario = RolModel.objects.filter(rol='4').first()
            if not rol_propietario:
                rol_propietario = RolModel.objects.create(rol='4')
            acc.id_rol_id = rol_propietario.id_rol
            acc.id_condominio_id = request.user.id_condominio_id
            acc.save()

            prop.id_usuario_id = acc.id
            prop.save()

            dataEmail = {'propietario': request.POST['nombre_propietario'], 'apto': aptos,
                         'password': dataPropietario['dni'], 'usuario': dataPropietario['dni']
                         }

            html_content = render_to_string('mails/mail.html', dataEmail)
            email = EmailMultiAlternatives('Esparta Suites: Información de Cuenta', html_content)
            email.attach_alternative(html_content, "text/html")
            email.to = [request.POST['email']]
            res = email.send()
            if res == 1:
                print("Correo enviado satisfactoriamente")

            messages.success(request,
                             '¡El propietario y su usuario han sido registrados de manera satisfactoria!',
                             extra_tags='alert-success')
            return True
        else:
            print(usuario.errors)
            primera_key = next(iter(usuario.errors))
            messages.warning(request,
                             usuario.errors[primera_key].as_text().replace('*', ''),
                             extra_tags='alert-danger')
    else:
        primera_key = next(iter(propietarios_form.errors))
        messages.warning(request,
                         propietarios_form.errors[primera_key].as_text().replace('*', ''),
                         extra_tags='alert-danger')

    return False


# ------------------------------ADMINISTRACION Y GESTION DE PROPIETARIOS------------------------------
@login_required
def admin_propietarios(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.filter(id_condominio=user.id_condominio_id)
    propietarios = Propietario.objects.filter(id_usuario__id_condominio_id=user.id_condominio_id)
    domicilios = Domicilio.objects.filter(id_propietario_id__isnull=True).select_related('id_propietario').order_by('-created_at')
    domicilios_disponibles = len(domicilios)

    torres = Torre.objects.all()
    propietarios_form = PropietariosForm()
    user_form = RegistrationForm()
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    cierre = Cierre_mes.objects.filter(id_condominio_id=user.id_condominio_id).order_by('fecha_cierre').last()
    movimientos = Movimientos_bancarios.objects.filter(
        id_banco__id_condominio_id=user.id_condominio_id,
        estado_movimiento=2,
    )
    if cierre:
        movimientos = movimientos.filter(created_at__gt=cierre.fecha_cierre)
    movimientos = movimientos.order_by('-fecha_movimiento', '-created_at', '-id_movimiento')
    for mov in movimientos:
        mov.emisor = ""
        recibo = Recibos.objects.filter(id_movimiento_id=mov.id_movimiento).select_related('id_deuda__id_domicilio__id_propietario').first()
        if recibo and recibo.id_deuda and recibo.id_deuda.id_domicilio and recibo.id_deuda.id_domicilio.id_propietario:
            mov.emisor = recibo.id_deuda.id_domicilio.id_propietario.nombre_propietario
        if not mov.emisor:
            ingreso = Ingresos.objects.filter(id_movimiento_id=mov.id_movimiento).select_related('id_propietario').first()
            if ingreso and ingreso.id_propietario:
                mov.emisor = ingreso.id_propietario.nombre_propietario
        if not mov.emisor:
            datos_transaccion = Datos_transaccion.objects.filter(id_movimiento_id=mov.id_movimiento).first()
            if datos_transaccion and datos_transaccion.nombre_titular:
                mov.emisor = datos_transaccion.nombre_titular
        if cierre and mov.created_at:
            mov.cerrado = mov.created_at <= cierre.fecha_cierre
        else:
            mov.cerrado = False

    if request.method == 'POST':
        if procesar_propietario_post(request):
            return HttpResponseRedirect(reverse('condominio_app:admin_propietarios'))

    return render(request, 'administrador/propietarios.html', {'propietarios': propietarios,
                                                               'propietarios_form': propietarios_form, 'user_form': user_form,
                                                               'domicilios': domicilios, 'movimientos': movimientos, 'torres': torres,
                                                               'conf': condominio, 'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro,
                                                               'domicilios_disponibles': domicilios_disponibles,
                                                               'show_propietarios_form': False,
                                                               'show_propietarios_list': True,
                                                               'show_movimientos_button': False})


@login_required
def admin_validacion_pagos(request):
    user = request.user
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.filter(id_condominio=user.id_condominio_id)
    propietarios = Propietario.objects.filter(id_usuario__id_condominio_id=user.id_condominio_id)
    domicilios = Domicilio.objects.filter(id_propietario_id__isnull=True).select_related('id_propietario').order_by('-created_at')
    domicilios_disponibles = len(domicilios)
    torres = Torre.objects.all()
    propietarios_form = PropietariosForm()
    user_form = RegistrationForm()

    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()
    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR
    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)
    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    cierre = Cierre_mes.objects.filter(id_condominio_id=user.id_condominio_id).order_by('fecha_cierre').last()
    movimientos = Movimientos_bancarios.objects.filter(
        id_banco__id_condominio_id=user.id_condominio_id,
    ).exclude(
        datos_transaccion__tipo_transaccion="GASTO",
    )
    if cierre:
        movimientos = movimientos.filter(created_at__gt=cierre.fecha_cierre)
    movimientos = movimientos.order_by('-fecha_movimiento', '-created_at', '-id_movimiento')
    for mov in movimientos:
        mov.emisor = ""
        recibo = Recibos.objects.filter(id_movimiento_id=mov.id_movimiento).select_related(
            'id_deuda__id_domicilio__id_propietario'
        ).first()
        if recibo and recibo.id_deuda and recibo.id_deuda.id_domicilio and recibo.id_deuda.id_domicilio.id_propietario:
            mov.emisor = recibo.id_deuda.id_domicilio.id_propietario.nombre_propietario
        if not mov.emisor:
            ingreso = Ingresos.objects.filter(id_movimiento_id=mov.id_movimiento).select_related(
                'id_propietario'
            ).first()
            if ingreso and ingreso.id_propietario:
                mov.emisor = ingreso.id_propietario.nombre_propietario
        if not mov.emisor:
            datos_transaccion = Datos_transaccion.objects.filter(id_movimiento_id=mov.id_movimiento).first()
            if datos_transaccion and datos_transaccion.nombre_titular:
                mov.emisor = datos_transaccion.nombre_titular
        if cierre and mov.created_at:
            mov.cerrado = mov.created_at <= cierre.fecha_cierre
        else:
            mov.cerrado = False

    return render(request, 'administrador/propietarios.html', {
        'propietarios': propietarios,
        'propietarios_form': propietarios_form,
        'user_form': user_form,
        'domicilios': domicilios,
        'movimientos': movimientos,
        'torres': torres,
        'conf': condominio,
        'tasa_bs': tasa_bs,
        'tasa_euro': tasa_euro,
        'domicilios_disponibles': domicilios_disponibles,
        'show_movimientos': True,
        'show_propietarios_form': False,
        'show_propietarios_list': False,
        'show_movimientos_button': False,
    })


@require_http_methods(['GET'])
def admin_propietarios_mov(request):
    if request.GET.get('respuesta') == 'Aprobado':

        user = request.user
        condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
        try:
            mov = Movimientos_bancarios.objects.get(id_movimiento=request.GET.get('id'))
        except Movimientos_bancarios.DoesNotExist:
            return JsonResponse({'mensaje': 'No se encontro el movimiento solicitado.'}, status=400)
        datos_mov = Datos_transaccion.objects.filter(id_movimiento_id=mov.id_movimiento).first()
        try:
            banco = Bancos.objects.get(id_banco=mov.id_banco_id)
        except Bancos.DoesNotExist:
            return JsonResponse({'mensaje': 'No se encontro el banco del movimiento.'}, status=400)

        if mov.monto_movimiento is None:
            return JsonResponse({'mensaje': 'El movimiento no tiene monto para aprobar.'}, status=400)
        mov.estado_movimiento = 0
        mov.updated_at = timezone.now()
        mov.credito_movimiento = (mov.credito_movimiento or 0) + mov.monto_movimiento
        mov.save()

        banco.creditos_banco = (banco.creditos_banco or 0) + mov.monto_movimiento
        banco.saldo_actual = (banco.saldo_actual or 0) + mov.monto_movimiento
        banco.save()

        prop = None
        ingreso_existente = Ingresos.objects.filter(id_movimiento=mov).select_related('id_propietario').first()
        if ingreso_existente and ingreso_existente.id_propietario:
            prop = ingreso_existente.id_propietario
        
        tipo_transaccion = datos_mov.tipo_transaccion if datos_mov else None
        if not tipo_transaccion:
            recibos_mov = Recibos.objects.filter(id_movimiento_id=mov.id_movimiento)
            if recibos_mov.filter(categoria_recibo__in=['ABONO', 'ABONADO']).exists():
                tipo_transaccion = 'ABONO'
            else:
                tipo_transaccion = 'PAGO'

        if tipo_transaccion == 'ABONO':
            recibo = Recibos.objects.filter(id_movimiento_id=request.GET.get('id')).select_related('id_deuda__id_domicilio__id_propietario').first()
            if recibo and recibo.id_deuda and recibo.id_deuda.id_domicilio:
                prop = recibo.id_deuda.id_domicilio.id_propietario
                if prop:
                    if mov.tipo_moneda == 'BS':
                        prop.saldo = (prop.saldo or 0) + mov.monto_movimiento
                    elif mov.tipo_moneda == 'USD':
                        prop.saldo_usd = (prop.saldo_usd or 0) + mov.monto_movimiento
                    elif mov.tipo_moneda == 'EUR':
                        prop.saldo_eur = (prop.saldo_eur or 0) + mov.monto_movimiento
                    prop.save()
            if not prop:
                propietarios = Propietario.objects.filter(id_usuario__id_condominio_id=user.id_condominio_id)
                for propietario in propietarios:
                    domicilios = Domicilio.objects.filter(id_propietario_id=propietario.id_propietario, id_condominio_id=condominio.id_condominio)
                    for domicilio in domicilios:
                        recibos_domicilio = Recibos.objects.filter(id_movimiento_id=request.GET.get('id'))
                        if recibos_domicilio.exists():
                            prop = propietario
                            if mov.tipo_moneda == 'BS':
                                prop.saldo = (prop.saldo or 0) + mov.monto_movimiento
                            elif mov.tipo_moneda == 'USD':
                                prop.saldo_usd = (prop.saldo_usd or 0) + mov.monto_movimiento
                            elif mov.tipo_moneda == 'EUR':
                                prop.saldo_eur = (prop.saldo_eur or 0) + mov.monto_movimiento
                            prop.save()
                            break
                    if prop:
                        break
        else:
            recibo = Recibos.objects.filter(id_movimiento_id=request.GET.get('id')).select_related('id_deuda__id_domicilio__id_propietario')
            prop = None
            for deuda_ind in recibo:
                if deuda_ind.id_deuda:
                    deuda_ind.id_deuda.updated_at = timezone.now()
                    deuda_ind.id_deuda.save()
                    if not prop and deuda_ind.id_deuda.id_domicilio:
                        prop = deuda_ind.id_deuda.id_domicilio.id_propietario

        if prop:
            mov.id_propietario = prop
            mov.save()

        ingreso = ingreso_existente if ingreso_existente else Ingresos()
        ingreso.tipo_ingreso = 'Pago de un propietario'
        ingreso.id_movimiento = mov
        if prop:
            ingreso.id_propietario = prop
        ingreso.save()

        if mov.tipo_moneda == 'BS':
            condominio.saldo_edificio += mov.monto_movimiento
        elif mov.tipo_moneda == 'USD':
            condominio.saldo_edificio_usd += mov.monto_movimiento
        elif mov.tipo_moneda == 'EUR':
            condominio.saldo_edificio_eur += mov.monto_movimiento
        else:
            print('Hubo un inconveniente al guardar el saldo del condominio.')

        condominio.save()

        messages.success(request,
                         '¡El movimiento fue aprobado con exito!',
                         extra_tags='alert-success')

        return JsonResponse({'mensaje': '¡El movimiento fue aprobado con exito!'})

    elif request.GET.get('respuesta') == 'Rechazado':

        mov = Movimientos_bancarios.objects.get(id_movimiento=request.GET.get('id'))
        recibo = Recibos.objects.filter(id_movimiento_id=request.GET.get('id')).select_related('id_deuda')
        for deudas in recibo:
            if deudas.id_deuda:
                deudas.id_deuda.is_active = True
                deudas.id_deuda.save()

        mov.estado_movimiento = 1
        mov.updated_at = timezone.now()
        mov.save()

        messages.warning(request,
                         '¡El movimiento fue rechazado con exito!',
                         extra_tags='alert-success')

        return JsonResponse({'mensaje': '¡El movimiento fue rechazado con exito!'})

    else:
        return JsonResponse({'mensaje': 'Ocurrio un error con los datos enviados.'})


@login_required
def admin_domicilios(request):

    if request.method == 'POST':
        user = request.user
        domicilio_form = DomicilioForm(data=request.POST)
        if domicilio_form.is_valid():
            dom = domicilio_form.save()

            if 'piso_domicilio' in request.POST:
                dom.id_torre_id = request.POST['piso_domicilio']

            if 'torres' in request.POST:
                dom.id_torre_id = request.POST['torres']

                dom.id_condominio_id = user.id_condominio
                dom.save()

            if float(request.POST['saldo']) < 0:
                deudas = Deudas(fecha_deuda=timezone.now().strftime("%Y-%m-%d"),tipo_deuda=2, monto_deuda=abs(float(request.POST['saldo'])), is_active=True,
                                created_at=timezone.now(),
                                updated_at=timezone.now(), id_domicilio=dom, tipo_moneda=Deudas.TipoMoneda.BS,
                                concepto_deuda="Deuda del propietario",
                                descripcion_deuda="Deuda inicial del propietario registrado",
                                is_moroso=False)
                            
                deudas.save()

            if float(request.POST['saldo_usd']) < 0:
                deudas = Deudas(fecha_deuda=timezone.now().strftime("%Y-%m-%d"),
                                tipo_deuda=2,
                                monto_deuda=abs(float(request.POST['saldo_usd'])), is_active=True,
                                created_at=timezone.now(),
                                updated_at=timezone.now(), id_domicilio=dom, tipo_moneda=Deudas.TipoMoneda.USD,
                                concepto_deuda="Deuda del propietario",
                                descripcion_deuda="Deuda inicial del propietario registrado",
                                is_moroso=False, id_condominio_id=user.id_condominio)
                deudas.save()

            if float(request.POST['saldo_eur']) < 0:
                deudas = Deudas(fecha_deuda=timezone.now().strftime("%Y-%m-%d"),
                                tipo_deuda=2,
                                monto_deuda=abs(float(request.POST['saldo_eur'])), is_active=True,
                                created_at=timezone.now(),
                                updated_at=timezone.now(), id_domicilio=dom, tipo_moneda=Deudas.TipoMoneda.EUR,
                                concepto_deuda="Deuda del propietario",
                                descripcion_deuda="Deuda inicial del propietario registrado",
                                is_moroso=False, id_condominio_id=user.id_condominio)
                deudas.save()

            messages.success(request, '¡El domicilio fue registrado con exito!', extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "domicilios"}))
                
        else:
            print(domicilio_form.errors)
            primera_key = next(iter(domicilio_form.errors))
            messages.warning(request,
                             domicilio_form.errors[primera_key].as_text().replace('*', ''),
                             extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "domicilios"}))

def admin_abono_deudas(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    conf = Condominio.objects.get(id_condominio=user.id_condominio_id)
    deudas_condominio = Deudas.objects.filter(tipo_deuda="1", id_deuda=id)
    deudas_propietario = Deudas.objects.filter(tipo_deuda="2", id_deuda=id).select_related('id_domicilio__id_propietario')
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    monto_deuda = 0
    saldo = 0
    saldo_usd = 0
    saldo_eur = 0

    if deudas_condominio.exists():
        deuda_condo = deudas_condominio
        deuda_prop = {}

        for deuda in deuda_condo:
            monto_deuda = deuda.monto_deuda
            saldo = conf.saldo_edificio
            saldo_usd = conf.saldo_edificio_usd
            saldo_eur = conf.saldo_edificio_eur
            tipo_moneda = deuda.tipo_moneda

    else:
        deuda_condo = {}
        deuda_prop = deudas_propietario

        for deuda in deuda_prop:
            monto_deuda = deuda.monto_deuda
            saldo = deuda.id_domicilio.saldo
            saldo_usd = deuda.id_domicilio.saldo_usd
            saldo_eur = deuda.id_domicilio.saldo_eur
            tipo_moneda = deuda.tipo_moneda

    if request.method == 'POST':

        siguiente = False

        if tipo_moneda == "BS":
            if monto_deuda > saldo:
                if request.POST['max_value'] == saldo:
                    if request.POST["abono"] < request.POST['max_value']:
                        siguiente = True
                    else:
                        messages.warning(request,
                                         'Los valores enviados no coinciden con los parametros preconfigurados.',
                                         extra_tags='alert-danger')
                else:
                    messages.warning(request, 'Los valores enviados no coinciden con los parametros preconfigurados.', extra_tags='alert-danger')
            else:
                if request.POST['max_value'] == monto_deuda:
                    if request.POST["abono"] < request.POST['max_value']:
                        siguiente = True
                    else:
                        messages.warning(request,
                                         'Los valores enviados no coinciden con los parametros preconfigurados.',
                                         extra_tags='alert-danger')
                else:
                    messages.warning(request, 'Los valores enviados no coinciden con los parametros preconfigurados.', extra_tags='alert-danger')

        elif tipo_moneda == "USD":
            if monto_deuda > saldo_usd:
                if request.POST['max_value'] == saldo_usd:
                    if request.POST["abono"] < request.POST['max_value']:
                        siguiente = True
                    else:
                        messages.warning(request,
                                         'Los valores enviados no coinciden con los parametros preconfigurados.',
                                         extra_tags='alert-danger')
                else:
                    messages.warning(request, 'Los valores enviados no coinciden con los parametros preconfigurados.', extra_tags='alert-danger')
            else:
                if request.POST['max_value'] == monto_deuda:
                    if request.POST["abono"] < request.POST['max_value']:
                        siguiente = True
                    else:
                        messages.warning(request,
                                         'Los valores enviados no coinciden con los parametros preconfigurados.',
                                         extra_tags='alert-danger')
                else:
                    messages.warning(request, 'Los valores enviados no coinciden con los parametros preconfigurados.', extra_tags='alert-danger')

        else:
            if monto_deuda > saldo_eur:
                if request.POST['max_value'] == saldo_eur:
                    if request.POST["abono"] < request.POST['max_value']:
                        siguiente = True
                    else:
                        messages.warning(request,
                                         'Los valores enviados no coinciden con los parametros preconfigurados.',
                                         extra_tags='alert-danger')
                else:
                    messages.warning(request, 'Los valores enviados no coinciden con los parametros preconfigurados.', extra_tags='alert-danger')
            else:
                if request.POST['max_value'] == monto_deuda:
                    if request.POST["abono"] < request.POST['max_value']:
                        siguiente = True
                    else:
                        messages.warning(request,
                                         'Los valores enviados no coinciden con los parametros preconfigurados.',
                                         extra_tags='alert-danger')
                else:
                    messages.warning(request, 'Los valores enviados no coinciden con los parametros preconfigurados.', extra_tags='alert-danger')

        if siguiente:
            if deudas_condominio.exists():
                for deuda in deudas_condominio:
                    if Decimal(request.POST["abono"]) < deuda.monto_deuda:
                        deuda.monto_deuda -= Decimal(request.POST["abono"])
                        deuda.save()
                    else:
                        deuda.is_active = False
                        deuda.save()

            else:
                for deuda in deudas_propietario:
                    if Decimal(request.POST["abono"]) < deuda.monto_deuda:
                        deuda.monto_deuda -= Decimal(request.POST["abono"])
                        deuda.save()
                    else:
                        deuda.is_active = False
                        deuda.save()

        return HttpResponseRedirect(reverse('condominio_app:admin_deudas'))

    return render(request, 'administrador/extras/abono_deudas.html', {'conf': conf, 'tasa_bs': tasa_bs,
                                                                       'deuda_condo': deuda_condo, 'deuda_prop':deuda_prop,
                                                                       'tasa_euro': tasa_euro})


# ------------------------------CONFIGURACION------------------------------
@login_required
def admin_configuracion(request, type=''):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.filter(id_condominio=user.id_condominio_id)
    precios = Precios.objects.filter(id_condominio_id=user.id_condominio_id)
    recargos_descuentos = Recargos_y_Descuentos.objects.filter(id_condominio_id=user.id_condominio_id)
    torres = Torre.objects.filter(id_condominio_id=user.id_condominio_id)
    bancos = Bancos.objects.filter(id_condominio_id=user.id_condominio_id)
    domicilios = Domicilio.objects.filter(id_condominio_id=user.id_condominio_id)
    domicilios_propietarios = Domicilio.objects.filter(
        id_condominio_id=user.id_condominio_id,
        id_propietario_id__isnull=True
    ).order_by('-created_at')
    propietarios = Propietario.objects.filter(id_usuario__id_condominio_id=user.id_condominio_id)

    config_form = CondominioForm()
    banco_form = BancosForm()
    torres_form = TorreForm()
    domicilio_form = DomicilioForm()
    precios_form = Establecimiento_preciosForm()
    tasas_form = Tasas_de_cambioForm()
    recargo_descuento_form = Recargos_y_DescuentosForm()
    propietarios_form = PropietariosForm()
    user_form = RegistrationForm()
    ultima_tasa = Tasas.objects.last()
    if not ultima_tasa and type != 'tasa':
        messages.warning(request, 'Configure las tasas de cambio antes de usar otros módulos de Configuración.', extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': 'tasa'}))
    today = timezone.now()
    if ultima_tasa:
        tasa_bs = ultima_tasa.tasa_BCV_USD
        tasa_euro = ultima_tasa.tasa_BCV_EUR
        tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                               today.strftime("%A"), tasa_bs, tasa_euro)
        tasa_bs = tasas['tasa_BCV_USD']
        tasa_euro = tasas['tasa_BCV_EUR']
    else:
        tasa_bs = 0
        tasa_euro = 0

    if request.method == 'POST':
        if request.POST.get('form_origen') == 'configuracion_propietarios':
            procesar_propietario_post(request)
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "condominio"}))

        if (request.POST['tlf_1'] == '') and (request.POST['tlf_2'] == ''):
            messages.warning(request,
                             'Ha ocurrido un error guardando la configuración. Debe colocar por lo menos 1 número de teléfono.',
                             extra_tags='alert-danger')

        if 'saldo_edificio' in request.POST and 'saldo_edificio_usd' in request.POST and 'saldo_edificio_eur' in request.POST:

            data = request.POST
            config_form = CondominioForm(data=data)

            if config_form.is_valid():

                nombre_condominio = request.POST['nombre_condominio']
                rif_condominio = request.POST['rif_condominio']
                codigo_tlf_1 = request.POST['codigo_tlf_1']
                tlf_1 = request.POST['tlf_1']
                codigo_tlf_2 = request.POST['codigo_tlf_2']
                tlf_2 = request.POST['tlf_2']
                tipo_condominio = request.POST['tipo_condominio']
                direccion_condominio = request.POST['direccion_condominio']
                email = request.POST['email']
                saldo_edificio = request.POST['saldo_edificio']
                saldo_usd = request.POST['saldo_edificio_usd']
                saldo_eur = request.POST['saldo_edificio_eur']
                raw_superficie = request.POST.get('superficie_total_m2', '').strip()
                try:
                    superficie_total_m2 = Decimal(raw_superficie.replace(',', '.')) if raw_superficie else None
                except (ValueError, Exception):
                    superficie_total_m2 = None

                defaults_condominio = {
                    'nombre_condominio': nombre_condominio,
                    'rif_condominio': rif_condominio,
                    'codigo_tlf_1': codigo_tlf_1,
                    'tlf_1': tlf_1, 'tipo_condominio': tipo_condominio,
                    'codigo_tlf_2': codigo_tlf_2,
                    'tlf_2': tlf_2,
                    'direccion_condominio': direccion_condominio,
                    'email': email,
                    'saldo_edificio': saldo_edificio,
                    'saldo_edificio_usd': saldo_usd,
                    'saldo_edificio_eur': saldo_eur,
                }
                if superficie_total_m2 is not None:
                    defaults_condominio['superficie_total_m2'] = superficie_total_m2

                # Se busca el objeto o se crea
                c, created = Condominio.objects.get_or_create(id_condominio=user.id_condominio_id, defaults=defaults_condominio)

                if created:
                    usuario = Usuario.objects.get(pk=user.pk)
                    usuario.id_condominio_id = c.id_condominio
                    usuario.save()
                else:
                    # Actualizar datos del condominio existente
                    for k, v in defaults_condominio.items():
                        setattr(c, k, v)

                # Banners del slider: guardar si se enviaron archivos
                if request.FILES.get('banner_1'):
                    c.banner_1 = request.FILES['banner_1']
                if request.FILES.get('banner_2'):
                    c.banner_2 = request.FILES['banner_2']
                if request.FILES.get('banner_3'):
                    c.banner_3 = request.FILES['banner_3']
                c.save()

                if created:
                    messages.success(request, '¡La configuración ha sido guardada de manera satisfactoria!',
                                     extra_tags='alert-success')
                else:
                    messages.success(request, '¡La configuración ha sido actualizada de manera satisfactoria!',
                                     extra_tags='alert-success')
                return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "condominio"}))
                
            else:
                primera_key = next(iter(config_form.errors))
                messages.warning(request,
                                 config_form.errors[primera_key].as_text().replace('*', ''),
                                 extra_tags='alert-danger')

        else:
            nombre_condominio = request.POST['nombre_condominio']
            rif_condominio = request.POST['rif_condominio']
            codigo_tlf_1 = request.POST['codigo_tlf_1']
            tlf_1 = request.POST['tlf_1']
            codigo_tlf_2 = request.POST['codigo_tlf_2']
            tlf_2 = request.POST['tlf_2']
            tipo_condominio = request.POST.get('tipo_condominio') or None
            direccion_condominio = request.POST['direccion_condominio']
            email = request.POST['email']
            raw_superficie = request.POST.get('superficie_total_m2', '').strip()
            try:
                superficie_total_m2 = Decimal(raw_superficie.replace(',', '.')) if raw_superficie else None
            except (ValueError, Exception):
                superficie_total_m2 = None

            c = Condominio.objects.get(id_condominio=user.id_condominio_id)
            c.nombre_condominio = nombre_condominio
            c.rif_condominio = rif_condominio
            c.codigo_tlf_1 = codigo_tlf_1
            c.tlf_1 = tlf_1
            c.codigo_tlf_2 = codigo_tlf_2
            c.tlf_2 = tlf_2
            c.tipo_condominio = tipo_condominio
            c.direccion_condominio = direccion_condominio
            c.email = email
            c.superficie_total_m2 = superficie_total_m2
            if request.FILES.get('banner_1'):
                c.banner_1 = request.FILES['banner_1']
            if request.FILES.get('banner_2'):
                c.banner_2 = request.FILES['banner_2']
            if request.FILES.get('banner_3'):
                c.banner_3 = request.FILES['banner_3']
            c.save()

            messages.success(request, '¡La configuración ha sido actualizada de manera satisfactoria!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "condominio"}))

    return render(request, 'administrador/configuracion.html', {'config_form': config_form, 'bancos_form': banco_form,
                                                                'torres_form': torres_form, 'precios_form': precios_form,
                                                                'tasas_form': tasas_form, 'recargo_descuento_form': recargo_descuento_form,
                                                                'domicilio_form': domicilio_form, 'recargos_descuento':recargos_descuentos,
                                                                'precio': precios, 'torres': torres, 'domicilios': domicilios,
                                                                'conf': condominio, 'tasa_bs': tasa_bs, 'bancos': bancos,
                                                                'tasa_euro': tasa_euro, 'type': type,
                                                                'propietarios': propietarios,
                                                                'propietarios_form': propietarios_form,
                                                                'user_form': user_form,
                                                                'domicilios_propietarios': domicilios_propietarios})


# ------------------------------CONFIGURACION SISTEMA------------------------------
@login_required
def configuracion_recargos_descuentos(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    recargo_descuento = Recargos_y_Descuentos.objects.all()
    try:
        condominio_obj = Condominio.objects.get(id_condominio=user.id_condominio_id)
        condominio = Condominio.objects.filter(id_condominio=user.id_condominio_id)
    except Condominio.DoesNotExist:
        messages.error(request, 'El condominio asociado a su usuario no existe. Por favor contacte al administrador.',
                      extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:home_admin'))
    
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    recargo_descuento_form = Recargos_y_DescuentosForm()

    if request.method == 'POST':
        if request.POST['dia_recargo'] <= request.POST['dia_descuento']:
            messages.warning(request,
                             'Ha ocurrido un error al establecer los porcentajes y días. El día de recargo no puede ser menor al día de descuento.',
                             extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:configurar_recargos_y_descuentos'))
        recargo_descuento_form = Recargos_y_DescuentosForm(data=request.POST)
        if recargo_descuento_form.is_valid():
            print("FORMULARIO VALIDO")
            rd, created = Recargos_y_Descuentos.objects.get_or_create(id_condominio_id=condominio_obj.id_condominio, defaults={
                'recargo_moratorio': request.POST['recargo_moratorio'], 'dia_recargo': request.POST['dia_recargo'],
                'descuento_pronto_pago': request.POST['descuento_pronto_pago'],
                'dia_descuento': request.POST['dia_descuento']})

            if created:
                messages.success(request, '¡Los porcentajes y días han sido establecidos de manera satisfactoria!',
                                 extra_tags='alert-success')
                return HttpResponseRedirect(reverse('condominio_app:configurar_recargos_y_descuentos'))
            else:
                Recargos_y_Descuentos.objects.filter(id_condominio_id=condominio_obj.id_condominio).update(
                    recargo_moratorio=request.POST['recargo_moratorio'], dia_recargo=request.POST['dia_recargo'],
                    descuento_pronto_pago=request.POST['descuento_pronto_pago'],
                    dia_descuento=request.POST['dia_descuento'], updated_at=timezone.now())

                messages.success(request, '¡Los porcentajes y días han sido actualizados de manera satisfactoria!',
                                 extra_tags='alert-success')
                return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "recargos"}))
        else:
            print("FORMULARIO NO VALIDO")
            messages.warning(request,
                             'Ha ocurrido un error al establecer los porcentajes y días. Verifique e intente de nuevo por favor.',
                             extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "recargos"}))

    return render(request, 'administrador/configuracion.html', {'conf': condominio, 'tasa_bs': tasa_bs,
                                                                'tasa_euro': tasa_euro,
                                                                'recargo_descuento_form': recargo_descuento_form,
                                                                'recargos_descuentos': recargo_descuento})


#
@login_required
def configuracion_tasas_de_cambio(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.filter(id_condominio=user.id_condominio_id)
    tasas_form = Tasas_de_cambioForm()
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_id = ultima_tasa.id
    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        tasas_form = Tasas_de_cambioForm(data=request.POST)
        if tasas_form.is_valid():
            print("TASAS DE CAMBIO ACTUALIZADAS")
            today = timezone.now()
            Tasas.objects.filter(pk=tasa_id).update(tasa_BCV_USD=request.POST['tasa_BCV_USD'],
                                                    tasa_BCV_EUR=request.POST['tasa_BCV_EUR'],
                                                    updated_at=timezone.now())
            messages.success(request, '¡Las tasas de cambio han sido actualizadas de manera satisfactoria!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "tasa"}))
        else:
            print("FORMULARIO NO VALIDO")
            messages.warning(request,
                             'Ha ocurrido un error al actualizar las tasas de cambio. Verifique e intente de nuevo por favor.',
                             extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "tasa"}))

    return render(request, 'administrador/configuracion.html',
                  {'conf': condominio, 'tasas_form': tasas_form,
                   'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro})


@login_required
def configuracion_establecimiento_precios(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    precio = Precios.objects.all()
    try:
        condominio_obj = Condominio.objects.get(id_condominio=user.id_condominio_id)
        condominio = Condominio.objects.filter(id_condominio=user.id_condominio_id)
    except Condominio.DoesNotExist:
        messages.error(request, 'El condominio asociado a su usuario no existe. Por favor contacte al administrador.',
                      extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:home_admin'))
    
    precios_form = Establecimiento_preciosForm()
    ultima_tasa = Tasas.objects.all().last()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    if request.method == 'POST':
        precios_form = Tasas_de_cambioForm(data=request.POST)
        if precios_form.is_valid():
            print("TASAS DE CAMBIO ACTUALIZADAS")
            p, created = Precios.objects.get_or_create(id_condominio_id=condominio_obj.id_condominio,
                                                       defaults={'maleteros': request.POST['maleteros'],
                                                                 'salon_fiesta': request.POST['salon_fiesta'],
                                                                 'otras_areas': request.POST['otras_areas']})

            if created:
                messages.success(request, '¡Los nuevos precios han sido establecidos de manera satisfactoria!',
                                 extra_tags='alert-success')
                return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "precios"}))
            else:
                Precios.objects.filter(id_condominio_id=condominio_obj.id_condominio).update(maleteros=request.POST['maleteros'],
                                                                     salon_fiesta=request.POST['salon_fiesta'],
                                                                     otras_areas=request.POST['otras_areas'],
                                                                     updated_at=timezone.now())

                messages.success(request, '¡Los precios han sido actualizados de manera satisfactoria!',
                                 extra_tags='alert-success')
                return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "precios"}))
        else:
            print("FORMULARIO NO VALIDO")
            messages.warning(request,
                             'Ha ocurrido un error al actualizar los precios. Verifique e intente de nuevo por favor.',
                             extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "precios"}))

    return render(request, 'administrador/configuracion.html', {'conf': condominio, 'precios_form': precios_form,
                                                                                    'precios': precio, 'tasa_bs': tasa_bs,
                                                                                    'tasa_euro': tasa_euro})


# ------------------------------ADMINISTRACION Y GESTIÓN DE CUENTAS ADMIN------------------------------
@login_required
def admin_cuentas(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    propietarios = Propietario.objects.filter(id_usuario__id_condominio_id=user.id_condominio_id)
    usuarios = Usuario.objects.filter(Q(id_rol__rol='0') | Q(id_rol__rol='1')) 
    user_form = RegistrationForm()
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        nombre_propietario = request.POST.get('nombre_propietario', '')
        tipo_dni = (request.POST.get('tipo_dni') or '').strip()
        dni = request.POST.get('dni', '')
        username = (request.POST.get('username') or '').upper()
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not tipo_dni:
            messages.warning(request, 'Debe escoger un tipo de documento (Venezolano, RIF, Jurídico, etc.).', extra_tags='alert-danger')
        elif password1 == password2:
            checkUser = Usuario.objects.filter(email=email)

            if checkUser.exists():
                messages.warning(request,
                                 'Ha ocurrido un error durante el registro. El correo electrónico ya esta en uso.',
                                 extra_tags='alert-danger')
            else:
                dataUsuario = {
                    'username': username,
                    'email': email,
                    'password1': password1
                }

                user_form = RegistrationForm(data=dataUsuario)

                if user_form.is_valid():
                    prop = Propietario(nombre_propietario=nombre_propietario, tipo_dni=tipo_dni, dni=dni)
                    prop.save()

                    acc = user_form.save(commit=False)
                    acc.set_password(password1)
                    acc.save()

                    getUsuario = Usuario.objects.get(email=email)

                    getUsuario.id_condominio_id = user.id_condominio_id
                    getUsuario.is_admin = True
                    getUsuario.save()

                    dataEmail = {
                        'administrador': nombre_propietario,
                        'usuario': username,
                        'password': password1
                    }

                    html_content = render_to_string('mails/admin-mail.html', dataEmail)

                    email = EmailMultiAlternatives('Esparta Suites: Información de Cuenta', html_content)
                    email.attach_alternative(html_content, "text/html")
                    email.to = [request.POST['email']]
                    res = email.send()
                    if (res == 1):
                        print("Correo enviado satisfactoriamente")

                    messages.success(request, 'El administrador ha sido creado exitosamente',
                                     extra_tags='alert-success')
                    return HttpResponseRedirect(reverse('condominio_app:admin_propietarios'))
                else:
                    messages.warning(request, 'Ha ocurrido un error durante el registro. Verifique e intente de nuevo.',
                                     extra_tags='alert-danger')
        else:
            messages.warning(request, 'Ha ocurrido un error durante el registro. Las contraseñas deben ser iguales.',
                             extra_tags='alert-danger')
    return render(request, 'administrador/cuentas.html', {'user_form': user_form, 'usuarios': usuarios,
                                                          'propietarios': propietarios, 'conf': condominio,
                                                          'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro})

# ------------------------------ADMINISTRACION Y GESTIÓN DE REPORTES------------------------------
def _parse_fecha_reporte(value):
    """Convierte string YYYY-MM-DD a date para que los templates |date funcionen."""
    if not value:
        return None
    try:
        return datetime.strptime(str(value).strip(), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


@login_required
def admin_reportes(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    bancos = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
    propietarios = Domicilio.objects.filter(id_propietario_id__isnull=False, id_propietario__id_usuario__id_condominio_id=user.id_condominio).select_related('id_propietario__id_usuario')
    propietarios_select = Propietario.objects.filter(id_usuario__id_condominio_id=condominio.id_condominio).select_related('id_usuario')
    cierre = Cierre_mes.objects.filter(id_condominio_id=user.id_condominio_id).order_by('fecha_cierre')

    ids_cierre = []
    cierres = []

    for mes in cierre:
        ids_cierre.append(mes.id_cierre)
        cierres.append(str(mes.pdf_cierre).split('cierres/cierre_mes')[1].replace('/', ' Realizado el ').replace('.', ':').replace('_', ' a las ').split(':pdf')[0])

    cierre_mensual = zip(ids_cierre, cierres)

    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        if request.POST['reporte'] == 'GASTOS':

            if request.POST['fecha_inicio'] > request.POST['fecha_fin']:
                messages.warning(request, 'La fecha inicial no puede ser mayor a la fecha final.',
                             extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
            else:

                template_path = 'PDF/gastos_pdf.html'
                data = {}

                inicio = request.POST['fecha_inicio']
                fin = request.POST['fecha_fin']

                total_bs = 0
                total_usd = 0
                total_eur = 0
                total_usd_en_bs = 0
                total_eur_en_bs = 0

                data['inicio'] = _parse_fecha_reporte(inicio) or inicio
                data['fin'] = _parse_fecha_reporte(fin) or fin
                data['datos_condominio'] = condominio
                data['gastos'] = Gastos.objects.filter(id_movimiento__fecha_movimiento__range=[inicio, fin],
                                                       id_movimiento__id_banco__id_condominio_id=condominio.id_condominio).select_related("id_movimiento__id_banco")
                data['bancos'] = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
                nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
                data['bancos_cabecera'] = [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in data['bancos']]
                data['tasas'] = Tasas.objects.all().last()

                for i in data['gastos']:
                    for j in data['bancos']:
                        if i.id_movimiento.id_banco_id == j.id_banco and j.tipo_moneda == 'BS':
                            total_bs += i.id_movimiento.monto_movimiento
                        elif i.id_movimiento.id_banco_id == j.id_banco and j.tipo_moneda == 'USD':
                            total_usd += i.id_movimiento.monto_movimiento
                        elif i.id_movimiento.id_banco_id == j.id_banco and j.tipo_moneda == 'EUR':
                            total_eur += i.id_movimiento.monto_movimiento

                data['total_bs'] = total_bs
                data['total_usd'] = total_usd
                data['total_eur'] = total_eur

                # Se calcula el total de dolares y euros en bolivares para la sumatoria de todo
                total_usd_en_bs = data['tasas'].tasa_BCV_USD * total_usd
                total_eur_en_bs = data['tasas'].tasa_BCV_EUR * total_eur

                data['total_usd_en_bs'] = total_usd_en_bs
                data['total_eur_en_bs'] = total_eur_en_bs

                # Se suman los valores para dar el resultado final en bolivares
                data['total_final_en_bs'] = total_usd_en_bs + total_eur_en_bs + total_bs

                data['fecha_generado'] = timezone.now()

                formato = (request.POST.get('formato') or 'PDF').upper()
                if formato == 'PDF':
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="reporte_gastos_{}_{}.pdf"'.format(inicio, fin)
                    template = get_template(template_path)
                    html = template.render(data)
                    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                elif formato == 'WORD':
                    template = get_template(template_path)
                    html = template.render(data)
                    response = HttpResponse(html, content_type='application/msword')
                    response['Content-Disposition'] = 'attachment; filename="reporte_gastos_{}_{}.doc"'.format(inicio, fin)
                    return response
                elif formato == 'EXCEL':
                    output = io.StringIO()
                    writer = csv.writer(output)
                    writer.writerow(['Fecha', 'Referencia', 'Descripción', 'Monto', 'Moneda', 'Banco'])
                    for gasto in data['gastos']:
                        moneda = 'BS'
                        for b in data['bancos']:
                            if gasto.id_movimiento.id_banco_id == b.id_banco:
                                moneda = b.tipo_moneda
                                break
                        _desc = (gasto.id_movimiento.descripcion_movimiento or gasto.id_movimiento.concepto_movimiento or '')
                        writer.writerow([
                            gasto.id_movimiento.fecha_movimiento,
                            gasto.id_movimiento.referencia_movimiento or '',
                            _desc,
                            gasto.id_movimiento.monto_movimiento,
                            moneda,
                            gasto.id_movimiento.id_banco.nombre_banco if gasto.id_movimiento.id_banco else '',
                        ])
                    response = HttpResponse(output.getvalue(), content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="reporte_gastos_{}_{}.csv"'.format(inicio, fin)
                    return response
                elif formato == 'TXT':
                    lines = ['Reporte de gastos', 'Fecha inicio: {}'.format(inicio), 'Fecha fin: {}'.format(fin),
                             'Total BS: {} | Total USD: {} | Total EUR: {}'.format(total_bs, total_usd, total_eur), '']
                    for gasto in data['gastos']:
                        moneda = 'BS'
                        for b in data['bancos']:
                            if gasto.id_movimiento.id_banco_id == b.id_banco:
                                moneda = b.tipo_moneda
                                break
                        _desc = (gasto.id_movimiento.descripcion_movimiento or gasto.id_movimiento.concepto_movimiento or '')
                        lines.append('{} | {} | {} | {} | {}'.format(
                            gasto.id_movimiento.fecha_movimiento, gasto.id_movimiento.referencia_movimiento or '-',
                            _desc, gasto.id_movimiento.monto_movimiento, moneda))
                    response = HttpResponse('\n'.join(lines), content_type='text/plain')
                    response['Content-Disposition'] = 'attachment; filename="reporte_gastos_{}_{}.txt"'.format(inicio, fin)
                    return response
                else:
                    messages.warning(request, 'Formato de reporte no valido.', extra_tags='alert-danger')
                    return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

        elif request.POST['reporte'] == 'INGRESOS':

            if request.POST['fecha_inicio'] > request.POST['fecha_fin']:
                messages.warning(request, 'La fecha inicial no puede ser mayor a la fecha final.',
                             extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
            else:

                template_path = 'PDF/ingresos_pdf.html'
                data = {}

                inicio = request.POST['fecha_inicio']
                fin = request.POST['fecha_fin']

                total_bs = 0
                total_usd = 0
                total_eur = 0
                total_usd_en_bs = 0
                total_eur_en_bs = 0

                data['inicio'] = _parse_fecha_reporte(inicio) or inicio
                data['fin'] = _parse_fecha_reporte(fin) or fin
                data['datos_condominio'] = condominio
                data['ingresos'] = Ingresos.objects.filter(id_movimiento__fecha_movimiento__range=[inicio, fin],
                                                            id_movimiento__id_banco__id_condominio_id=condominio.id_condominio,
                                                            id_movimiento__estado_movimiento=0).select_related("id_movimiento__id_banco")
                data['bancos'] = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
                nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
                data['bancos_cabecera'] = [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in data['bancos']]
                data['propietarios'] = Propietario.objects.filter(id_usuario__id_condominio_id=condominio.id_condominio).select_related('id_usuario')
                data['tasas'] = Tasas.objects.all().last()

                for banco in data['bancos']:
                    data['movimientos'] = Movimientos_bancarios.objects.filter(id_banco_id=banco.id_banco)

                for i in data['ingresos']:
                    for j in data['bancos']:
                        if i.id_movimiento.id_banco_id == j.id_banco and j.tipo_moneda == 'BS':
                            total_bs += i.id_movimiento.monto_movimiento
                        elif i.id_movimiento.id_banco_id == j.id_banco and j.tipo_moneda == 'USD':
                            total_usd += i.id_movimiento.monto_movimiento
                        elif i.id_movimiento.id_banco_id == j.id_banco and j.tipo_moneda == 'EUR':
                            total_eur += i.id_movimiento.monto_movimiento

                data['total_bs'] = total_bs
                data['total_usd'] = total_usd
                data['total_eur'] = total_eur

                total_usd_en_bs = data['tasas'].tasa_BCV_USD * total_usd
                total_eur_en_bs = data['tasas'].tasa_BCV_EUR * total_eur

                data['total_usd_en_bs'] = total_usd_en_bs
                data['total_eur_en_bs'] = total_eur_en_bs

                # Se suman los valores para dar el resultado final en bolivares
                data['total_final_en_bs'] = total_usd_en_bs + total_eur_en_bs + total_bs

                data['fecha_generado'] = timezone.now()

                formato = (request.POST.get('formato') or 'PDF').upper()
                if formato == 'PDF':
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="reporte_ingresos_{}_{}.pdf"'.format(inicio, fin)
                    template = get_template(template_path)
                    html = template.render(data)
                    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                elif formato == 'WORD':
                    template = get_template(template_path)
                    html = template.render(data)
                    response = HttpResponse(html, content_type='application/msword')
                    response['Content-Disposition'] = 'attachment; filename="reporte_ingresos_{}_{}.doc"'.format(inicio, fin)
                    return response
                elif formato == 'EXCEL':
                    output = io.StringIO()
                    writer = csv.writer(output)
                    writer.writerow(['Fecha', 'Referencia', 'Descripción', 'Monto', 'Moneda', 'Banco', 'Propietario'])
                    for ingreso in data['ingresos']:
                        moneda = 'BS'
                        for b in data['bancos']:
                            if ingreso.id_movimiento.id_banco_id == b.id_banco:
                                moneda = b.tipo_moneda
                                break
                        _desc = (ingreso.id_movimiento.descripcion_movimiento or ingreso.id_movimiento.concepto_movimiento or '')
                        writer.writerow([
                            ingreso.id_movimiento.fecha_movimiento,
                            ingreso.id_movimiento.referencia_movimiento or '',
                            _desc,
                            ingreso.id_movimiento.monto_movimiento,
                            moneda,
                            ingreso.id_movimiento.id_banco.nombre_banco if ingreso.id_movimiento.id_banco else '',
                            (ingreso.id_propietario.nombre_propietario if getattr(ingreso, 'id_propietario', None) else '') or '',
                        ])
                    response = HttpResponse(output.getvalue(), content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="reporte_ingresos_{}_{}.csv"'.format(inicio, fin)
                    return response
                elif formato == 'TXT':
                    lines = ['Reporte de ingresos', 'Fecha inicio: {}'.format(inicio), 'Fecha fin: {}'.format(fin),
                             'Total BS: {} | Total USD: {} | Total EUR: {}'.format(total_bs, total_usd, total_eur), '']
                    for ingreso in data['ingresos']:
                        moneda = 'BS'
                        for b in data['bancos']:
                            if ingreso.id_movimiento.id_banco_id == b.id_banco:
                                moneda = b.tipo_moneda
                                break
                        _desc = (ingreso.id_movimiento.descripcion_movimiento or ingreso.id_movimiento.concepto_movimiento or '')
                        lines.append('{} | {} | {} | {} | {}'.format(
                            ingreso.id_movimiento.fecha_movimiento, ingreso.id_movimiento.referencia_movimiento or '-',
                            _desc, ingreso.id_movimiento.monto_movimiento, moneda))
                    response = HttpResponse('\n'.join(lines), content_type='text/plain')
                    response['Content-Disposition'] = 'attachment; filename="reporte_ingresos_{}_{}.txt"'.format(inicio, fin)
                    return response
                else:
                    messages.warning(request, 'Formato de reporte no valido.', extra_tags='alert-danger')
                    return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

        elif request.POST['reporte'] == 'BANCOS':
                
            if request.POST['fecha_inicio'] > request.POST['fecha_fin']:
                messages.warning(request, 'La fecha inicial no puede ser mayor a la fecha final.',
                             extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
            else:

                template_path = 'PDF/estado_de_cuenta_pdf.html'
                data = {}

                inicio = request.POST['fecha_inicio']
                fin = request.POST['fecha_fin']
                banco_select = request.POST['banco_select']

                total_bs = 0
                total_usd = 0
                total_eur = 0
                total_usd_en_bs = 0
                total_eur_en_bs = 0
                nombre_banco = ""
                numero_cuenta = ""

                data['inicio'] = _parse_fecha_reporte(inicio) or inicio
                data['fin'] = _parse_fecha_reporte(fin) or fin
                data['datos_condominio'] = condominio
                data['bancos'] = Bancos.objects.filter(id_banco=banco_select, id_condominio_id=condominio.id_condominio)
                todos_bancos = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
                nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
                data['bancos_cabecera'] = [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in todos_bancos]
                data['movimientos'] = Movimientos_bancarios.objects.filter(id_banco_id=banco_select, fecha_movimiento__range=[inicio, fin], estado_movimiento=0).select_related('id_banco', 'id_propietario')

                for x in data['bancos']:
                    data['fecha_creacion'] = x.created_at.strftime("%d/%m/%Y")

                # data['creacion']
                data['nro_bank'] = len(data['bancos'])

                data['total_bs'] = total_bs
                data['total_usd'] = total_usd
                data['total_eur'] = total_eur

                # # Se calcula el total de dolares y euros en bolivares para la sumatoria de todo
                # for k in data['tasas']:
                #     total_usd_en_bs = k.tasa_BCV_USD * total_usd
                #     total_eur_en_bs = k.tasa_BCV_EUR * total_eur

                # Guardamos el nombre del banco
                for b in data['bancos']:
                    nombre_banco = b.nombre_banco
                    n = b.nro_cuenta or ''
                    numero_cuenta = '-'.join(n[i:i + 4] for i in range(0, len(n), 4)) if n else ''

                data['nombre_banco'] = nombre_banco
                data['numero_cuenta'] = numero_cuenta

                data['total_usd_en_bs'] = total_usd_en_bs
                data['total_eur_en_bs'] = total_eur_en_bs

                # Se suman los valores para dar el resultado final en bolivares
                data['total_final_en_bs'] = total_usd_en_bs + total_eur_en_bs + total_bs

                data['fecha_generado'] = timezone.now()

                formato = (request.POST.get('formato') or 'PDF').upper()
                if formato == 'PDF':
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="estado_de_cuenta_{}_{}_{}.pdf"'.format(
                        nombre_banco.replace(' ', '_'), inicio, fin)
                    template = get_template(template_path)
                    html = template.render(data)
                    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                elif formato == 'WORD':
                    template = get_template(template_path)
                    html = template.render(data)
                    response = HttpResponse(html, content_type='application/msword')
                    response['Content-Disposition'] = 'attachment; filename="estado_de_cuenta_{}_{}_{}.doc"'.format(
                        nombre_banco.replace(' ', '_'), inicio, fin)
                    return response
                elif formato == 'EXCEL':
                    output = io.StringIO()
                    writer = csv.writer(output)
                    writer.writerow(['Fecha', 'Referencia', 'Descripción', 'Debito', 'Credito', 'Emisor'])
                    for mov in data['movimientos']:
                        _d = (mov.descripcion_movimiento or mov.concepto_movimiento or '')
                        writer.writerow([
                            mov.fecha_movimiento,
                            mov.referencia_movimiento or '',
                            _d,
                            mov.debito_movimiento or '',
                            mov.credito_movimiento or '',
                            mov.emisor or mov.banco_emisor or '',
                        ])
                    response = HttpResponse(output.getvalue(), content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="estado_de_cuenta_{}_{}_{}.csv"'.format(
                        nombre_banco.replace(' ', '_'), inicio, fin)
                    return response
                elif formato == 'TXT':
                    lines = ['Estado de cuenta - {}'.format(nombre_banco), 'Fecha inicio: {}'.format(inicio), 'Fecha fin: {}'.format(fin), '']
                    for mov in data['movimientos']:
                        _d = (mov.descripcion_movimiento or mov.concepto_movimiento or '')
                        lines.append('{} | {} | {} | {} | {}'.format(
                            mov.fecha_movimiento, mov.referencia_movimiento or '-',
                            _d, mov.debito_movimiento or '', mov.credito_movimiento or ''))
                    response = HttpResponse('\n'.join(lines), content_type='text/plain')
                    response['Content-Disposition'] = 'attachment; filename="estado_de_cuenta_{}_{}_{}.txt"'.format(
                        nombre_banco.replace(' ', '_'), inicio, fin)
                    return response
                else:
                    messages.warning(request, 'Formato de reporte no valido.', extra_tags='alert-danger')
                    return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

        elif request.POST['reporte'] == 'MOVIMIENTOS':
                
            if request.POST['fecha_inicio'] > request.POST['fecha_fin']:
                messages.warning(request, 'La fecha inicial no puede ser mayor a la fecha final.',
                             extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
            else:

                template_path = 'PDF/movimientos_bancarios_pdf.html'
                data = {}

                inicio = request.POST['fecha_inicio']
                fin = request.POST['fecha_fin']
                banco_select = request.POST['banco_select']
                nombre_banco = ""
                numero_cuenta = ""

                data['inicio'] = _parse_fecha_reporte(inicio) or inicio
                data['fin'] = _parse_fecha_reporte(fin) or fin
                data['datos_condominio'] = condominio
                data['ingresos'] = Ingresos.objects.filter(id_movimiento__fecha_movimiento__range=[inicio, fin],
                                                            id_movimiento__id_banco__id_condominio_id=condominio.id_condominio, id_movimiento__id_banco_id=banco_select).select_related("id_movimiento__id_banco")
                data['gastos'] = Gastos.objects.filter(id_movimiento__fecha_movimiento__range=[inicio, fin],
                                                            id_movimiento__id_banco__id_condominio_id=condominio.id_condominio, id_movimiento__id_banco_id=banco_select).select_related("id_movimiento__id_banco")
                data['bancos'] = Bancos.objects.filter(id_banco=banco_select)
                data['fecha_generado'] = timezone.now()
                todos_bancos = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
                nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
                data['bancos_cabecera'] = [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in todos_bancos]

                # Guardamos el nombre del banco
                for b in data['bancos']:
                    nombre_banco = b.nombre_banco
                    n = b.nro_cuenta or ''
                    numero_cuenta = '-'.join(n[i:i + 4] for i in range(0, len(n), 4)) if n else ''

                data['nombre_banco'] = nombre_banco
                data['numero_cuenta'] = numero_cuenta

                formato = (request.POST.get('formato') or 'PDF').upper()
                nom_archivo = nombre_banco.replace(' ', '_')
                if formato == 'PDF':
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="consulta_movimientos_{}_{}_{}.pdf"'.format(nom_archivo, inicio, fin)
                    template = get_template(template_path)
                    html = template.render(data)
                    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                elif formato == 'WORD':
                    template = get_template(template_path)
                    html = template.render(data)
                    response = HttpResponse(html, content_type='application/msword')
                    response['Content-Disposition'] = 'attachment; filename="consulta_movimientos_{}_{}_{}.doc"'.format(nom_archivo, inicio, fin)
                    return response
                elif formato == 'EXCEL':
                    output = io.StringIO()
                    writer = csv.writer(output)
                    writer.writerow(['Tipo', 'Fecha', 'Referencia', 'Descripción', 'Monto'])
                    for ingreso in data['ingresos']:
                        _d = (ingreso.id_movimiento.descripcion_movimiento or ingreso.id_movimiento.concepto_movimiento or '')
                        writer.writerow(['INGRESO', ingreso.id_movimiento.fecha_movimiento, ingreso.id_movimiento.referencia_movimiento or '', _d, ingreso.id_movimiento.monto_movimiento])
                    for gasto in data['gastos']:
                        _d = (gasto.id_movimiento.descripcion_movimiento or gasto.id_movimiento.concepto_movimiento or '')
                        writer.writerow(['GASTO', gasto.id_movimiento.fecha_movimiento, gasto.id_movimiento.referencia_movimiento or '', _d, gasto.id_movimiento.monto_movimiento])
                    response = HttpResponse(output.getvalue(), content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="consulta_movimientos_{}_{}_{}.csv"'.format(nom_archivo, inicio, fin)
                    return response
                elif formato == 'TXT':
                    lines = ['Consulta de movimientos - {}'.format(nombre_banco), 'Desde {} hasta {}'.format(inicio, fin), '']
                    for ingreso in data['ingresos']:
                        _d = (ingreso.id_movimiento.descripcion_movimiento or ingreso.id_movimiento.concepto_movimiento or '')
                        lines.append('INGRESO | {} | {} | {} | {}'.format(ingreso.id_movimiento.fecha_movimiento, ingreso.id_movimiento.referencia_movimiento or '-', _d, ingreso.id_movimiento.monto_movimiento))
                    for gasto in data['gastos']:
                        _d = (gasto.id_movimiento.descripcion_movimiento or gasto.id_movimiento.concepto_movimiento or '')
                        lines.append('GASTO | {} | {} | {} | {}'.format(gasto.id_movimiento.fecha_movimiento, gasto.id_movimiento.referencia_movimiento or '-', _d, gasto.id_movimiento.monto_movimiento))
                    response = HttpResponse('\n'.join(lines), content_type='text/plain')
                    response['Content-Disposition'] = 'attachment; filename="consulta_movimientos_{}_{}_{}.txt"'.format(nom_archivo, inicio, fin)
                    return response
                else:
                    messages.warning(request, 'Formato de reporte no valido.', extra_tags='alert-danger')
                    return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

        elif request.POST['reporte'] == 'PROPIETARIOS':
            template_path = 'PDF/propietarios_pdf.html'
            data = {}

            prop = Propietario.objects.filter(
                id_usuario__id_condominio_id=user.id_condominio_id
            ).prefetch_related('prop_dom').order_by('nombre_propietario')

            data['propietarios'] = prop
            data['datos_condominio'] = condominio
            data['fecha_generado'] = timezone.now()
            todos_bancos = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
            nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
            data['bancos_cabecera'] = [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in todos_bancos]

            # Solo inmuebles del condominio actual (evita mostrar inmuebles de otros condominios)
            domicilios_flat = []
            for p in prop:
                doms_condominio = p.prop_dom.filter(id_condominio_id=condominio.id_condominio)
                domicilios_flat.extend(doms_condominio)
            total_bs = sum(Decimal(str(d.saldo or 0)) for d in domicilios_flat)
            total_usd = sum(Decimal(str(d.saldo_usd or 0)) for d in domicilios_flat)
            total_eur = sum(Decimal(str(d.saldo_eur or 0)) for d in domicilios_flat)
            data['total_domicilios_bs'] = total_bs
            data['total_domicilios_usd'] = total_usd
            data['total_domicilios_eur'] = total_eur

            # Estructura con alícuota calculada por domicilio (solo inmuebles de este condominio)
            propietarios_con_datos = []
            for p in prop:
                doms_condominio = p.prop_dom.filter(id_condominio_id=condominio.id_condominio)
                domicilios_con_alicuota = [
                    (d, _alicuota_para_display(d)) for d in doms_condominio
                ]
                propietarios_con_datos.append({
                    'propietario': p,
                    'domicilios_con_alicuota': domicilios_con_alicuota,
                })
            data['propietarios_con_datos'] = propietarios_con_datos

            data['usuarios'] = Usuario.objects.filter(id_condominio_id=user.id_condominio_id)
            # data['inicio']       = inicio
            # data['fin']          = fin
            # data['movimientos']  = Movimientos_bancarios.objects.filter(fecha_movimiento__range=[inicio, fin], id_banco_id=banco_select)
            # data['bancos']       = Bancos.objects.filter(id_banco=banco_select)

            data['fecha_generado'] = timezone.now()

            formato = (request.POST.get('formato') or 'PDF').upper()
            if formato == 'PDF':
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="reporte_propietarios.pdf"'
                template = get_template(template_path)
                html = template.render(data)
                pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
                if pisa_status.err:
                    return HttpResponse('We had some errors <pre>' + html + '</pre>')
                return response
            elif formato == 'WORD':
                template = get_template(template_path)
                html = template.render(data)
                response = HttpResponse(html, content_type='application/msword')
                response['Content-Disposition'] = 'attachment; filename="reporte_propietarios.doc"'
                return response
            elif formato == 'EXCEL':
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(['Propietario', 'Inmueble', 'Tipo', 'Alicuota', 'm2', 'Saldo BS', 'Saldo USD', 'Saldo EUR'])
                for p in prop:
                    for dom in p.prop_dom.filter(id_condominio_id=condominio.id_condominio):
                        alic = _alicuota_para_display(dom)
                        writer.writerow([
                            p.nombre_propietario,
                            dom.nombre_domicilio,
                            dom.tipo_domicilio or '',
                            round(alic, 4) if alic is not None else '',
                            dom.size_domicilio or '',
                            dom.saldo or '',
                            dom.saldo_usd or '',
                            dom.saldo_eur or '',
                        ])
                response = HttpResponse(output.getvalue(), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="reporte_propietarios.csv"'
                return response
            elif formato == 'TXT':
                lines = ['Reporte de propietarios', 'Total BS: {} | Total USD: {} | Total EUR: {}'.format(total_bs, total_usd, total_eur), '']
                for p in prop:
                    lines.append('Propietario: {}'.format(p.nombre_propietario))
                    for dom in p.prop_dom.filter(id_condominio_id=condominio.id_condominio):
                        alic = _alicuota_para_display(dom)
                        lines.append('  - {} | {} | Alicuota: {} | m2: {} | BS: {} | USD: {} | EUR: {}'.format(
                            dom.nombre_domicilio, dom.tipo_domicilio or '-', round(alic, 4) if alic is not None else '-', dom.size_domicilio or '-',
                            dom.saldo or 0, dom.saldo_usd or 0, dom.saldo_eur or 0))
                    lines.append('')
                response = HttpResponse('\n'.join(lines), content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename="reporte_propietarios.txt"'
                return response
            else:
                messages.warning(request, 'Formato de reporte no valido.', extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

        elif request.POST['reporte'] == 'DEUDAS':
            if request.POST['fecha_inicio'] > request.POST['fecha_fin']:
                messages.warning(request, 'La fecha inicial no puede ser mayor a la fecha final.',
                             extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
            else:
                inicio = request.POST['fecha_inicio']
                fin = request.POST['fecha_fin']
                formato = (request.POST.get('formato') or 'PDF').upper()

                deudas = Deudas.objects.filter(
                    id_domicilio__id_condominio_id=condominio.id_condominio,
                    tipo_deuda="2",
                    is_active=True,
                    fecha_deuda__range=[inicio, fin]
                ).select_related('id_domicilio', 'id_domicilio__id_propietario')

                total_bs = 0
                total_usd = 0
                total_eur = 0
                for deuda in deudas:
                    if deuda.tipo_moneda == 'BS':
                        total_bs += deuda.monto_deuda
                    elif deuda.tipo_moneda == 'USD':
                        total_usd += deuda.monto_deuda
                    elif deuda.tipo_moneda == 'EUR':
                        total_eur += deuda.monto_deuda

                todos_bancos = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
                nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
                data = {
                    'inicio': _parse_fecha_reporte(inicio) or inicio,
                    'fin': _parse_fecha_reporte(fin) or fin,
                    'deudas': deudas,
                    'total_bs': total_bs,
                    'total_usd': total_usd,
                    'total_eur': total_eur,
                    'fecha_generado': timezone.now(),
                    'condominio': condominio,
                    'datos_condominio': condominio,
                    'bancos_cabecera': [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in todos_bancos],
                }

                template_path = 'PDF/deudas_general_pdf.html'

                if formato == 'PDF':
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="reporte_deudas_{}_{}.pdf"'.format(inicio, fin)
                    template = get_template(template_path)
                    html = template.render(data)
                    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                elif formato == 'WORD':
                    template = get_template(template_path)
                    html = template.render(data)
                    response = HttpResponse(html, content_type='application/msword')
                    response['Content-Disposition'] = 'attachment; filename="reporte_deudas_{}_{}.doc"'.format(inicio, fin)
                    return response
                elif formato == 'EXCEL':
                    output = io.StringIO()
                    writer = csv.writer(output)
                    writer.writerow(['Propietario', 'Domicilio', 'Descripción', 'Monto', 'Moneda', 'Fecha', 'Moroso'])
                    for deuda in deudas:
                        propietario_nombre = ''
                        if deuda.id_domicilio and deuda.id_domicilio.id_propietario:
                            propietario_nombre = deuda.id_domicilio.id_propietario.nombre_propietario
                        _desc = (deuda.descripcion_deuda or deuda.concepto_deuda or '')
                        writer.writerow([
                            propietario_nombre,
                            deuda.id_domicilio.nombre_domicilio if deuda.id_domicilio else '',
                            _desc,
                            deuda.monto_deuda,
                            deuda.tipo_moneda,
                            deuda.fecha_deuda,
                            'Si' if deuda.is_active else 'No',
                        ])
                    response = HttpResponse(output.getvalue(), content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="reporte_deudas_{}_{}.csv"'.format(inicio, fin)
                    return response
                elif formato == 'TXT':
                    lines = [
                        'Reporte de deudas',
                        'Fecha inicio: {}'.format(inicio),
                        'Fecha fin: {}'.format(fin),
                        'Total BS: {}'.format(total_bs),
                        'Total USD: {}'.format(total_usd),
                        'Total EUR: {}'.format(total_eur),
                        '',
                    ]
                    for deuda in deudas:
                        propietario_nombre = ''
                        if deuda.id_domicilio and deuda.id_domicilio.id_propietario:
                            propietario_nombre = deuda.id_domicilio.id_propietario.nombre_propietario
                        _desc = (deuda.descripcion_deuda or deuda.concepto_deuda or '')
                        lines.append(
                            '{} | {} | {} | {} | {} | {} | {}'.format(
                                propietario_nombre,
                                deuda.id_domicilio.nombre_domicilio if deuda.id_domicilio else '',
                                _desc,
                                deuda.monto_deuda,
                                deuda.tipo_moneda,
                                deuda.fecha_deuda,
                                'Si' if deuda.is_active else 'No'
                            )
                        )
                    response = HttpResponse('\n'.join(lines), content_type='text/plain')
                    response['Content-Disposition'] = 'attachment; filename="reporte_deudas_{}_{}.txt"'.format(inicio, fin)
                    return response
                else:
                    messages.warning(request, 'Formato de reporte no valido.', extra_tags='alert-danger')
                    return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

        elif request.POST['reporte'] == 'ESTADO_CUENTA':
            if request.POST['fecha_inicio'] > request.POST['fecha_fin']:
                messages.warning(request, 'La fecha inicial no puede ser mayor a la fecha final.',
                             extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
            else:
                inicio = request.POST['fecha_inicio']
                fin = request.POST['fecha_fin']
                propietario_id = request.POST.get('propietario_select')
                formato = (request.POST.get('formato') or 'PDF').upper()

                if not propietario_id:
                    messages.warning(request, 'Debe seleccionar un propietario.', extra_tags='alert-danger')
                    return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

                propietario = Propietario.objects.filter(
                    id_propietario=propietario_id,
                    id_usuario__id_condominio_id=condominio.id_condominio
                ).select_related('id_usuario').first()

                if not propietario:
                    messages.warning(request, 'No se encontro el propietario.', extra_tags='alert-danger')
                    return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

                # Solo inmuebles de este propietario en este condominio (no otros propietarios ni otros condominios)
                domicilios_propietario = Domicilio.objects.filter(
                    id_propietario_id=propietario_id,
                    id_condominio_id=condominio.id_condominio
                ).values_list('id_domicilio', flat=True)
                deudas = Deudas.objects.filter(
                    id_domicilio_id__in=domicilios_propietario,
                    tipo_deuda="2",
                    fecha_deuda__range=[inicio, fin]
                ).select_related('id_domicilio').order_by('id_domicilio', 'fecha_deuda')

                total_bs = 0
                total_usd = 0
                total_eur = 0
                total_pendiente_bs = 0
                total_pendiente_usd = 0
                total_pendiente_eur = 0
                for deuda in deudas:
                    if deuda.tipo_moneda == 'BS':
                        total_bs += deuda.monto_deuda
                        if deuda.is_active:
                            total_pendiente_bs += deuda.monto_deuda
                    elif deuda.tipo_moneda == 'USD':
                        total_usd += deuda.monto_deuda
                        if deuda.is_active:
                            total_pendiente_usd += deuda.monto_deuda
                    elif deuda.tipo_moneda == 'EUR':
                        total_eur += deuda.monto_deuda
                        if deuda.is_active:
                            total_pendiente_eur += deuda.monto_deuda

                todos_bancos = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
                nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
                data = {
                    'inicio': _parse_fecha_reporte(inicio) or inicio,
                    'fin': _parse_fecha_reporte(fin) or fin,
                    'deudas': deudas,
                    'propietario': propietario,
                    'total_bs': total_bs,
                    'total_usd': total_usd,
                    'total_eur': total_eur,
                    'total_pendiente_bs': total_pendiente_bs,
                    'total_pendiente_usd': total_pendiente_usd,
                    'total_pendiente_eur': total_pendiente_eur,
                    'fecha_generado': timezone.now(),
                    'condominio': condominio,
                    'datos_condominio': condominio,
                    'bancos_cabecera': [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in todos_bancos],
                }

                template_path = 'PDF/estado_cuenta_pdf.html'

                # Enviar por correo al propietario (PDF adjunto)
                if request.POST.get('enviar_correo'):
                    email_destino = None
                    if propietario.id_usuario_id:
                        usuario = propietario.id_usuario
                        if getattr(usuario, 'email', None):
                            email_destino = usuario.email
                    if not email_destino:
                        messages.warning(
                            request,
                            'El propietario no tiene correo electrónico asociado. No se puede enviar el reporte.',
                            extra_tags='alert-danger',
                        )
                        return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
                    try:
                        template = get_template(template_path)
                        html = template.render(data)
                        pdf_buffer = io.BytesIO()
                        pisa_status = pisa.CreatePDF(html, dest=pdf_buffer, link_callback=link_callback)
                        if pisa_status.err:
                            messages.warning(request, 'Error al generar el PDF para el correo.', extra_tags='alert-danger')
                            return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
                        pdf_buffer.seek(0)
                        nombre_condominio = getattr(condominio, 'nombre_condominio', 'Condominio') or 'Condominio'
                        asunto = 'Estado de cuenta - {}'.format(nombre_condominio)
                        cuerpo = 'Estimado/a {}, adjuntamos su estado de cuenta del {} al {}. Saludos.'.format(
                            propietario.nombre_propietario,
                            data['inicio'].strftime('%d/%m/%Y') if hasattr(data['inicio'], 'strftime') else data['inicio'],
                            data['fin'].strftime('%d/%m/%Y') if hasattr(data['fin'], 'strftime') else data['fin'],
                        )
                        email = EmailMultiAlternatives(asunto, cuerpo, settings.EMAIL_HOST_USER, [email_destino])
                        email.attach('Estado_cuenta_{}_{}.pdf'.format(propietario.nombre_propietario.replace(' ', '_'), inicio), pdf_buffer.getvalue(), 'application/pdf')
                        email.send(fail_silently=False)
                        messages.success(request, 'Estado de cuenta enviado por correo a {}.'.format(email_destino), extra_tags='alert-success')
                    except Exception as e:
                        messages.warning(
                            request,
                            'No se pudo enviar el correo: {}.'.format(str(e)),
                            extra_tags='alert-danger',
                        )
                    return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

                if formato == 'PDF':
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="estado_cuenta_{}_{}_{}.pdf"'.format(propietario_id, inicio, fin)
                    template = get_template(template_path)
                    html = template.render(data)
                    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
                    if pisa_status.err:
                        return HttpResponse('We had some errors <pre>' + html + '</pre>')
                    return response
                elif formato == 'WORD':
                    template = get_template(template_path)
                    html = template.render(data)
                    response = HttpResponse(html, content_type='application/msword')
                    response['Content-Disposition'] = 'attachment; filename="estado_cuenta_{}_{}_{}.doc"'.format(propietario_id, inicio, fin)
                    return response
                elif formato == 'EXCEL':
                    output = io.StringIO()
                    writer = csv.writer(output)
                    writer.writerow(['Domicilio', 'Descripción', 'Monto', 'Moneda', 'Fecha', 'Estado'])
                    for deuda in deudas:
                        _desc = (deuda.descripcion_deuda or deuda.concepto_deuda or '')
                        writer.writerow([
                            deuda.id_domicilio.nombre_domicilio if deuda.id_domicilio else '',
                            _desc,
                            deuda.monto_deuda,
                            deuda.tipo_moneda,
                            deuda.fecha_deuda,
                            'Pendiente' if deuda.is_active else 'Pagada',
                        ])
                    response = HttpResponse(output.getvalue(), content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="estado_cuenta_{}_{}_{}.csv"'.format(propietario_id, inicio, fin)
                    return response
                elif formato == 'TXT':
                    lines = [
                        'Estado de cuenta del propietario',
                        'Propietario: {}'.format(propietario.nombre_propietario),
                        'Fecha inicio: {}'.format(inicio),
                        'Fecha fin: {}'.format(fin),
                        'Total BS: {}'.format(total_bs),
                        'Total USD: {}'.format(total_usd),
                        'Total EUR: {}'.format(total_eur),
                        'Pendiente BS: {}'.format(total_pendiente_bs),
                        'Pendiente USD: {}'.format(total_pendiente_usd),
                        'Pendiente EUR: {}'.format(total_pendiente_eur),
                        '',
                    ]
                    for deuda in deudas:
                        _desc = (deuda.descripcion_deuda or deuda.concepto_deuda or '')
                        lines.append(
                            '{} | {} | {} | {} | {} | {}'.format(
                                deuda.id_domicilio.nombre_domicilio if deuda.id_domicilio else '',
                                _desc,
                                deuda.monto_deuda,
                                deuda.tipo_moneda,
                                deuda.fecha_deuda,
                                'Pendiente' if deuda.is_active else 'Pagada'
                            )
                        )
                    response = HttpResponse('\n'.join(lines), content_type='text/plain')
                    response['Content-Disposition'] = 'attachment; filename="estado_cuenta_{}_{}_{}.txt"'.format(propietario_id, inicio, fin)
                    return response
                else:
                    messages.warning(request, 'Formato de reporte no valido.', extra_tags='alert-danger')
                    return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

        elif request.POST['reporte'] == 'INMUEBLE':
            if request.POST['fecha_inicio_inm'] > request.POST['fecha_fin_inm']:
                messages.warning(request, 'La fecha inicial no puede ser mayor a la fecha final.',
                             extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
            inicio_inm = request.POST['fecha_inicio_inm']
            fin_inm = request.POST['fecha_fin_inm']
            domicilio_id = request.POST.get('inmueble_select')
            formato_inm = (request.POST.get('formato') or 'PDF').upper()
            if not domicilio_id:
                messages.warning(request, 'Debe seleccionar un inmueble.', extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
            domicilio = Domicilio.objects.filter(
                id_domicilio=domicilio_id,
                id_condominio_id=condominio.id_condominio
            ).select_related('id_propietario', 'id_torre').first()
            if not domicilio:
                messages.warning(request, 'No se encontró el inmueble.', extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
            deudas_inm = Deudas.objects.filter(
                id_domicilio_id=domicilio_id,
                tipo_deuda="2",
                fecha_deuda__range=[inicio_inm, fin_inm]
            ).select_related('id_domicilio').order_by('fecha_deuda')
            total_bs_inm = sum(d.monto_deuda for d in deudas_inm if d.tipo_moneda == 'BS')
            total_usd_inm = sum(d.monto_deuda for d in deudas_inm if d.tipo_moneda == 'USD')
            total_eur_inm = sum(d.monto_deuda for d in deudas_inm if d.tipo_moneda == 'EUR')
            total_pend_bs = sum(d.monto_deuda for d in deudas_inm if d.tipo_moneda == 'BS' and d.is_active)
            total_pend_usd = sum(d.monto_deuda for d in deudas_inm if d.tipo_moneda == 'USD' and d.is_active)
            total_pend_eur = sum(d.monto_deuda for d in deudas_inm if d.tipo_moneda == 'EUR' and d.is_active)
            todos_bancos = Bancos.objects.filter(id_condominio_id=condominio.id_condominio)
            nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
            alicuota_inm = _alicuota_para_display(domicilio)
            data_inm = {
                'inicio': _parse_fecha_reporte(inicio_inm) or inicio_inm,
                'fin': _parse_fecha_reporte(fin_inm) or fin_inm,
                'domicilio': domicilio,
                'alicuota_display': alicuota_inm,
                'deudas': deudas_inm,
                'total_bs': total_bs_inm, 'total_usd': total_usd_inm, 'total_eur': total_eur_inm,
                'total_pendiente_bs': total_pend_bs, 'total_pendiente_usd': total_pend_usd, 'total_pendiente_eur': total_pend_eur,
                'fecha_generado': timezone.now(),
                'condominio': condominio, 'datos_condominio': condominio,
                'bancos_cabecera': [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in todos_bancos],
            }
            template_path_inm = 'PDF/inmueble_pdf.html'

            # Enviar por correo al propietario del inmueble (solo PDF; nombre distinto a enviar_correo de Estado de cuenta)
            if request.POST.get('enviar_correo_inmueble'):
                propietario_inm = domicilio.id_propietario
                email_destino = None
                if propietario_inm and propietario_inm.id_usuario_id:
                    usuario_inm = propietario_inm.id_usuario
                    if getattr(usuario_inm, 'email', None):
                        email_destino = usuario_inm.email
                if not email_destino:
                    messages.warning(
                        request,
                        'El inmueble no tiene propietario con correo electrónico. No se puede enviar el reporte.',
                        extra_tags='alert-danger',
                    )
                    return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
                try:
                    template = get_template(template_path_inm)
                    html = template.render(data_inm)
                    pdf_buffer = io.BytesIO()
                    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer, link_callback=link_callback)
                    if pisa_status.err:
                        messages.warning(request, 'Error al generar el PDF para el correo.', extra_tags='alert-danger')
                        return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))
                    pdf_buffer.seek(0)
                    nombre_condominio = getattr(condominio, 'nombre_condominio', 'Condominio') or 'Condominio'
                    nombre_inm = (domicilio.nombre_domicilio or 'Inmueble').replace(' ', '_')
                    asunto = 'Reporte por inmueble - {} - {}'.format(nombre_condominio, nombre_inm)
                    cuerpo = 'Estimado/a {}, adjuntamos el reporte del inmueble {} del {} al {}. Saludos.'.format(
                        propietario_inm.nombre_propietario,
                        domicilio.nombre_domicilio or domicilio_id,
                        data_inm['inicio'].strftime('%d/%m/%Y') if hasattr(data_inm['inicio'], 'strftime') else data_inm['inicio'],
                        data_inm['fin'].strftime('%d/%m/%Y') if hasattr(data_inm['fin'], 'strftime') else data_inm['fin'],
                    )
                    email_msg = EmailMultiAlternatives(asunto, cuerpo, settings.EMAIL_HOST_USER, [email_destino])
                    email_msg.attach('Reporte_inmueble_{}_{}_{}.pdf'.format(nombre_inm, inicio_inm, fin_inm), pdf_buffer.getvalue(), 'application/pdf')
                    email_msg.send(fail_silently=False)
                    messages.success(request, 'Reporte por inmueble enviado por correo a {}.'.format(email_destino), extra_tags='alert-success')
                except Exception as e:
                    messages.warning(
                        request,
                        'No se pudo enviar el correo: {}.'.format(str(e)),
                        extra_tags='alert-danger',
                    )
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

            if formato_inm == 'PDF':
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="reporte_inmueble_{}_{}_{}.pdf"'.format(domicilio_id, inicio_inm, fin_inm)
                template = get_template(template_path_inm)
                html = template.render(data_inm)
                pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
                if pisa_status.err:
                    return HttpResponse('We had some errors <pre>' + html + '</pre>')
                return response
            elif formato_inm == 'WORD':
                template = get_template(template_path_inm)
                html = template.render(data_inm)
                response = HttpResponse(html, content_type='application/msword')
                response['Content-Disposition'] = 'attachment; filename="reporte_inmueble_{}_{}_{}.doc"'.format(domicilio_id, inicio_inm, fin_inm)
                return response
            elif formato_inm == 'EXCEL':
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(['Descripción', 'Monto', 'Moneda', 'Fecha', 'Estado'])
                for deuda in deudas_inm:
                    _desc = (deuda.descripcion_deuda or deuda.concepto_deuda or '')
                    writer.writerow([
                        _desc, deuda.monto_deuda,
                        deuda.tipo_moneda, deuda.fecha_deuda, 'Pendiente' if deuda.is_active else 'Pagada',
                    ])
                response = HttpResponse(output.getvalue(), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="reporte_inmueble_{}_{}_{}.csv"'.format(domicilio_id, inicio_inm, fin_inm)
                return response
            elif formato_inm == 'TXT':
                lines = [
                    'Reporte del inmueble: {}'.format(domicilio.nombre_domicilio),
                    'Propietario: {}'.format(domicilio.id_propietario.nombre_propietario if domicilio.id_propietario else '—'),
                    'Fecha inicio: {} - Fecha fin: {}'.format(inicio_inm, fin_inm),
                    'Total BS: {} | Total USD: {} | Total EUR: {}'.format(total_bs_inm, total_usd_inm, total_eur_inm),
                    'Pendiente BS: {} | Pendiente USD: {} | Pendiente EUR: {}'.format(total_pend_bs, total_pend_usd, total_pend_eur),
                    '',
                ]
                for deuda in deudas_inm:
                    _desc = (deuda.descripcion_deuda or deuda.concepto_deuda or '')
                    lines.append('{} | {} | {} | {} | {}'.format(
                        _desc, deuda.monto_deuda,
                        deuda.tipo_moneda, deuda.fecha_deuda, 'Pendiente' if deuda.is_active else 'Pagada'
                    ))
                response = HttpResponse('\n'.join(lines), content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename="reporte_inmueble_{}_{}_{}.txt"'.format(domicilio_id, inicio_inm, fin_inm)
                return response
            else:
                messages.warning(request, 'Formato de reporte no valido.', extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:admin_reportes'))

        elif request.POST['reporte'] == 'CIERRE_MES':

            if request.POST['cierre'] == "CONDOMINIO":

                print(request.POST['cierre_del_mes'])
                cierre_seleccionado = Cierre_mes.objects.get(id_cierre=request.POST['cierre_del_mes'])
                print(cierre_seleccionado)

                with cierre_seleccionado.pdf_cierre.open(mode='rb') as f:
                    response = HttpResponse(f.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="'+str(cierre_seleccionado.pdf_cierre).split('cierres/')[1]+'"'
                    return response
            
            else:

                cierre = Cierre_mes.objects.get(id_cierre=request.POST['cierre_del_mes'])
                prop = Propietario.objects.get(id_propietario=request.POST['propietario_seleccionado'])

                pdf = cierre_propietario(request, prop, cierre, user)

                return pdf

    else:
        pass

    inmuebles_select = Domicilio.objects.filter(
        id_condominio_id=condominio.id_condominio
    ).select_related('id_propietario', 'id_torre').order_by('id_torre', 'nombre_domicilio')
    return render(request, 'administrador/reportes.html', {
        'conf': condominio, 'propietarios': propietarios,
        'propietarios_select': propietarios_select,
        'inmuebles_select': inmuebles_select,
        'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro,
        'bancos': bancos, 'cierre': cierre_mensual,
    })

# ------------------------------ADMINISTRACION Y GESTIÓN DE CIERRES MENSUALES------------------------------
@login_required
def admin_cierres(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.filter(id_condominio=user.id_condominio_id)
    datos_condominio = condominio.first()
    ultima_tasa = Tasas.objects.last()
    if not ultima_tasa:
        messages.warning(request, 'Configure las tasas de cambio antes de ver el cierre del mes.', extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': 'tasa'}))
    cierre_mes = Cierre_mes.objects.filter(id_condominio_id=user.id_condominio_id)
    deudas = Deudas.objects.filter(
        is_active=True,
        id_domicilio__id_condominio_id=user.id_condominio_id,
        monto_deuda__gt=0
    )
    deudas_prop = deudas.filter(tipo_deuda="2").values('id_domicilio_id').distinct()
    today = timezone.now()

    hoy = datetime.now().date()

    # Calcular la fecha hace 5 meses
    cinco_meses_atras = hoy - timedelta(days=30 * 6)

    # Consulta
    resultados_ingresos = Ingresos.objects.filter(id_movimiento__fecha_movimiento__gte=cinco_meses_atras, id_movimiento__fecha_movimiento__lte=hoy, id_movimiento__id_banco__id_condominio_id=user.id_condominio_id).annotate(mes=TruncMonth('id_movimiento__fecha_movimiento')).values('mes').annotate(total=Sum('id_movimiento__monto_movimiento')).order_by('mes')
    resultados_gastos = Gastos.objects.filter(id_movimiento__fecha_movimiento__gte=cinco_meses_atras, id_movimiento__fecha_movimiento__lte=hoy, id_movimiento__id_banco__id_condominio_id=user.id_condominio_id).annotate(
        mes=TruncMonth('id_movimiento__fecha_movimiento')).values('mes').annotate(total=Sum('id_movimiento__monto_movimiento')).order_by('mes')

    mes = ["", "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE",
           "NOVIEMBRE", "DICIEMBRE"]

    total_ingreso = []
    total_gasto = []
    mes_final = []

    i_monto = []
    g_monto = []

    # Imprimir resultados (Ingresos)
    for resultado in resultados_ingresos:
        total_ingreso.append(resultado['total'])

    for resultado in resultados_gastos:
        total_gasto.append(resultado['total'])
        mes_final.append(mes[int(resultado['mes'].strftime('%m'))])

    # Imprimir resultados (Gastos)
    for i in total_ingreso:
        i_monto.append(float(i))

    for g in total_gasto:
        g_monto.append(float(g))

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    resultado_ingreso = {}
    resultado_gasto = {}
    resultado_fondo = {}

    if cierre_mes.exists():
        ultimo_cierre = cierre_mes.last()
        resultado_ingreso = Ingresos.objects.filter(
            id_movimiento__created_at__gt=ultimo_cierre.fecha_cierre,
            id_movimiento__estado_movimiento=0,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento")
        movimientos_propietarios = Movimientos_bancarios.objects.filter(
            estado_movimiento=0,
            id_banco__id_condominio_id=user.id_condominio_id,
            created_at__gt=ultimo_cierre.fecha_cierre,
        ).select_related("id_banco")
        resultado_gasto = Gastos.objects.filter(
            id_movimiento__created_at__gt=ultimo_cierre.fecha_cierre,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento")
        resultado_fondo = Fondos.objects.filter(
            id_movimiento__created_at__gt=ultimo_cierre.fecha_cierre,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento")

        if resultado_ingreso.exists() and resultado_gasto.exists():
            pass
        else:
            messages.warning(request, 'Para cerrar el mes se debe tener al menos un ingreso y un gasto.',
                                 extra_tags='alert-danger')
    else:
        filtro_condo = {'id_movimiento__id_banco__id_condominio_id': user.id_condominio_id}
        ingresos = Ingresos.objects.filter(**filtro_condo).first()
        gastos = Gastos.objects.filter(**filtro_condo).first()
        fondos = Fondos.objects.filter(**filtro_condo).first()

        if ingresos is None or gastos is None:
            messages.warning(request,
                             'Para cerrar el mes se debe tener al menos un ingreso y un gasto.',
                             extra_tags='alert-danger')

        resultado_ingreso = Ingresos.objects.filter(
            id_movimiento__created_at__gte=ingresos.id_movimiento.created_at,
            id_movimiento__estado_movimiento=0,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento") if ingresos else Ingresos.objects.none()
        movimientos_propietarios = Movimientos_bancarios.objects.filter(
            estado_movimiento=0,
            id_banco__id_condominio_id=user.id_condominio_id,
            created_at__gte=ingresos.id_movimiento.created_at,
        ).select_related("id_banco") if ingresos else Movimientos_bancarios.objects.none()
        resultado_gasto = Gastos.objects.filter(
            id_movimiento__created_at__gte=gastos.id_movimiento.created_at,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento") if gastos else Gastos.objects.none()
        resultado_fondo = Fondos.objects.filter(
            id_movimiento__created_at__gte=fondos.id_movimiento.created_at,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento") if fondos else Fondos.objects.none()

    # Evitar duplicar ingresos: si un movimiento ya tiene Ingreso, no repetirlo
    ingreso_ids = resultado_ingreso.values_list('id_movimiento_id', flat=True)
    movimientos_propietarios = movimientos_propietarios.exclude(id_movimiento__in=ingreso_ids)

    if request.method == 'POST':
        template_path = 'PDF/cierre_mes.html'
        data = {}

        # Gastos
        gastos_lista = []
        for gasto in resultado_gasto:

            _desc = (gasto.id_movimiento.descripcion_movimiento or gasto.id_movimiento.concepto_movimiento or '')
            if gasto.id_movimiento.tipo_moneda == "BS":
                data_gasto = {'descripcion': _desc, 'monto': gasto.id_movimiento.monto_movimiento}
                gastos_lista.append(data_gasto)
            elif gasto.id_movimiento.tipo_moneda == "USD":
                monto_usd = Decimal(gasto.id_movimiento.monto_movimiento) / Decimal(tasa_bs)
                data_gasto = {'descripcion': _desc, 'monto': monto_usd}
                gastos_lista.append(data_gasto)
            elif gasto.id_movimiento.tipo_moneda == "EUR":
                monto_eur = Decimal(gasto.id_movimiento.monto_movimiento) / Decimal(tasa_euro)
                data_gasto = {'descripcion': _desc, 'monto': monto_eur}
                gastos_lista.append(data_gasto)

        data['gastos'] = gastos_lista
        data['t_gastos'] = resultado_gasto.filter(id_movimiento__tipo_moneda__iexact="BS").aggregate(Sum('id_movimiento__monto_movimiento'))
        data['t_gastos_USD'] = resultado_gasto.filter(id_movimiento__tipo_moneda__iexact="USD").aggregate(Sum('id_movimiento__monto_movimiento'))
        data['t_gastos_EUR'] = resultado_gasto.filter(id_movimiento__tipo_moneda__iexact="EUR").aggregate(Sum('id_movimiento__monto_movimiento'))

        # Ingresos
        ingresos_lista = []
        for ingreso in resultado_ingreso:
            
            _desc = (ingreso.id_movimiento.descripcion_movimiento or ingreso.id_movimiento.concepto_movimiento or '')
            if ingreso.id_movimiento.tipo_moneda == "BS":
                data_ingreso = {'descripcion': _desc, 'monto': ingreso.id_movimiento.monto_movimiento}
                ingresos_lista.append(data_ingreso)
            elif ingreso.id_movimiento.tipo_moneda == "USD":
                monto_usd = Decimal(ingreso.id_movimiento.monto_movimiento) / Decimal(tasa_bs)
                data_ingreso = {'descripcion': _desc, 'monto': monto_usd}
                ingresos_lista.append(data_ingreso)
            elif ingreso.id_movimiento.tipo_moneda == "EUR":
                monto_eur = Decimal(ingreso.id_movimiento.monto_movimiento) / Decimal(tasa_euro)
                data_ingreso = {'descripcion': _desc, 'monto': monto_eur}
                ingresos_lista.append(data_ingreso)

        for mov_prop in movimientos_propietarios:
            _desc = (mov_prop.descripcion_movimiento or mov_prop.concepto_movimiento or '')
            if mov_prop.tipo_moneda == "BS":
                ingresos_lista.append({'descripcion': _desc, 'monto': mov_prop.monto_movimiento})
            elif mov_prop.tipo_moneda == "USD":
                ingresos_lista.append({'descripcion': _desc, 'monto': Decimal(mov_prop.monto_movimiento) / Decimal(tasa_bs)})
            elif mov_prop.tipo_moneda == "EUR":
                ingresos_lista.append({'descripcion': _desc, 'monto': Decimal(mov_prop.monto_movimiento) / Decimal(tasa_euro)})

        data['ingresos'] = ingresos_lista
        total_ingresos_bs = resultado_ingreso.filter(id_movimiento__tipo_moneda__iexact="BS").aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0
        total_ingresos_usd = resultado_ingreso.filter(id_movimiento__tipo_moneda__iexact="USD").aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0
        total_ingresos_eur = resultado_ingreso.filter(id_movimiento__tipo_moneda__iexact="EUR").aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0
        total_mov_prop_bs = movimientos_propietarios.filter(tipo_moneda__iexact="BS").aggregate(Sum('monto_movimiento'))['monto_movimiento__sum'] or 0
        total_mov_prop_usd = movimientos_propietarios.filter(tipo_moneda__iexact="USD").aggregate(Sum('monto_movimiento'))['monto_movimiento__sum'] or 0
        total_mov_prop_eur = movimientos_propietarios.filter(tipo_moneda__iexact="EUR").aggregate(Sum('monto_movimiento'))['monto_movimiento__sum'] or 0
        data['t_ingresos'] = {'id_movimiento__monto_movimiento__sum': total_ingresos_bs + total_mov_prop_bs}
        data['t_ingresos_USD'] = {'id_movimiento__monto_movimiento__sum': total_ingresos_usd + total_mov_prop_usd}
        data['t_ingresos_EUR'] = {'id_movimiento__monto_movimiento__sum': total_ingresos_eur + total_mov_prop_eur}

        # Establecimiento de Precios
        if Precios.objects.exists():
            precios = Precios.objects.all().last()
            precio = [precios.maleteros, precios.salon_fiesta, precios.otras_areas]
        else:
            messages.warning(request, 'Por favor establezca los precios antes de hacer un cierre.',
                             extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "precios"}))

        tipo_precio = ["Maleteros", "Mantenimiento de Áreas", "Mantenimiento del Edificio", "Jardinería"]
        data['precios'] = zip(precio, tipo_precio)

        # Recargos y Descuentos
        if Recargos_y_Descuentos.objects.exists():
            recargos_descuentos = Recargos_y_Descuentos.objects.all().last()
        else:
            messages.warning(request, 'Por favor establezca los recargos y descuentos antes de hacer un cierre.',
                             extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "recargos"}))

        recargo_descuento = [str(recargos_descuentos.recargo_moratorio) + "%", recargos_descuentos.dia_recargo,
                             str(recargos_descuentos.descuento_pronto_pago) + "%",
                             recargos_descuentos.dia_descuento]

        tipo_recargo_descuento = ["Recargo por morosidad", "Dia de aplicación de la mororsidad",
                                  "Descuento por pronto pago", "Dia de finalización del descuento"]
        data['recargos_descuentos'] = zip(recargo_descuento, tipo_recargo_descuento)

        # Deudas
        monto_deuda_condo = 0
        monto_deuda_prop = 0
        total_deuda = 0

        # Por Condominio
        if Deudas.objects.exists():
            monto_deuda_condo = Deudas.objects.filter(is_active=True, tipo_deuda="1").aggregate(Sum('monto_deuda'))['monto_deuda__sum']
            if monto_deuda_condo is None:
                monto_deuda_condo = 0

        # Por Propietario
        if Deudas.objects.exists():
            monto_deuda_prop = Deudas.objects.filter(is_active=True, tipo_deuda="2").aggregate(Sum('monto_deuda'))['monto_deuda__sum']
            if monto_deuda_prop is None:
                monto_deuda_prop = 0

        total_deuda = monto_deuda_condo + monto_deuda_prop

        data['monto_deuda_condo'] = monto_deuda_condo
        data['monto_deuda_prop'] = monto_deuda_prop
        data['t_deudas'] = total_deuda

        fondo_reserva = 0
        fondo_operacional = 0
        fondo_otros = 0

        # Fondos (solo del condominio del usuario)
        filtro_fondos_condo = {'id_movimiento__id_banco__id_condominio_id': user.id_condominio_id}
        monto_reserva = Fondos.objects.filter(tipo_fondo="RESERVA", **filtro_fondos_condo).distinct()
        if monto_reserva.exists():
            fondo_reserva = monto_reserva.aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
            data['fondo_reserva'] = fondo_reserva
        else:
            data['fondo_reserva'] = 0

        monto_operacional = Fondos.objects.filter(tipo_fondo="OPERACIONAL", **filtro_fondos_condo).distinct()
        if monto_operacional.exists():
            fondo_operacional = monto_operacional.aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
            data['fondo_operacional'] = fondo_operacional
        else:
            data['fondo_operacional'] = 0

        monto_otros = Fondos.objects.filter(tipo_fondo="OTROS FONDOS", **filtro_fondos_condo).distinct()
        if monto_otros.exists():
            fondo_otros = monto_otros.aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
            data['fondo_otros'] = fondo_otros
        else:
            data['fondo_otros'] = 0
        monto_prestaciones = Fondos.objects.filter(tipo_fondo="PRESTACIONES", **filtro_fondos_condo).distinct()
        if monto_prestaciones.exists():
            data['fondo_prestaciones'] = monto_prestaciones.aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
        else:
            data['fondo_prestaciones'] = 0

        total_fondos = (fondo_reserva or 0) + (fondo_operacional or 0) + (fondo_otros or 0) + (data['fondo_prestaciones'] or 0)

        # Nivel 1: Fondo de reserva (10% gastos del mes), saldos anteriores, gastos bancarios
        t_g_bs = data['t_gastos']['id_movimiento__monto_movimiento__sum'] or 0
        t_g_usd = data['t_gastos_USD']['id_movimiento__monto_movimiento__sum'] or 0
        t_g_eur = data['t_gastos_EUR']['id_movimiento__monto_movimiento__sum'] or 0
        total_gastos_mes_bs = Decimal(str(t_g_bs)) + Decimal(str(t_g_usd)) / Decimal(str(tasa_bs)) + Decimal(str(t_g_eur)) / Decimal(str(tasa_euro))
        apartado_reserva = (total_gastos_mes_bs * Decimal('0.10')).quantize(Decimal('0.01'))
        data['apartado_fondo_reserva'] = apartado_reserva
        if cierre_mes.exists():
            ultimo_cierre = cierre_mes.last()
            saldo_ant_reserva = Fondos.objects.filter(
                tipo_fondo="RESERVA", **filtro_fondos_condo,
                id_movimiento__created_at__lte=ultimo_cierre.fecha_cierre
            ).aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
            saldo_ant_prestaciones = Fondos.objects.filter(
                tipo_fondo="PRESTACIONES", **filtro_fondos_condo,
                id_movimiento__created_at__lte=ultimo_cierre.fecha_cierre
            ).aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
        else:
            saldo_ant_reserva = Decimal('0')
            saldo_ant_prestaciones = Decimal('0')
        data['saldo_anterior_reserva'] = saldo_ant_reserva
        data['saldo_anterior_prestaciones'] = saldo_ant_prestaciones
        data['saldo_actual_reserva'] = (Decimal(str(saldo_ant_reserva)) + apartado_reserva).quantize(Decimal('0.01'))
        # Apartado prestaciones es manual; saldo actual = anterior + 0 por ahora
        data['apartado_prestaciones'] = Decimal('0')
        data['saldo_actual_prestaciones'] = saldo_ant_prestaciones
        if cierre_mes.exists():
            gastos_bancarios_bs = Gastos.objects.filter(
                tipo_gasto='GASTOS BANCARIOS',
                id_movimiento__created_at__gt=cierre_mes.last().fecha_cierre,
                id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
            ).aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
        else:
            gastos_bancarios_bs = 0
        data['total_gastos_bancarios_mes'] = gastos_bancarios_bs

        # Diferencia
        if data['t_gastos']['id_movimiento__monto_movimiento__sum'] is None:
            data['t_gastos']['id_movimiento__monto_movimiento__sum'] = 0

        if data['t_ingresos']['id_movimiento__monto_movimiento__sum'] is None:
            data['t_ingresos']['id_movimiento__monto_movimiento__sum'] = 0

        if data['t_gastos_USD']['id_movimiento__monto_movimiento__sum'] is None:
            data['t_gastos_USD']['id_movimiento__monto_movimiento__sum'] = 0

        if data['t_ingresos_USD']['id_movimiento__monto_movimiento__sum'] is None:
            data['t_ingresos_USD']['id_movimiento__monto_movimiento__sum'] = 0

        if data['t_gastos_EUR']['id_movimiento__monto_movimiento__sum'] is None:
            data['t_gastos_EUR']['id_movimiento__monto_movimiento__sum'] = 0

        if data['t_ingresos_EUR']['id_movimiento__monto_movimiento__sum'] is None:
            data['t_ingresos_EUR']['id_movimiento__monto_movimiento__sum'] = 0

        data["Diferencia"] = data['t_ingresos']['id_movimiento__monto_movimiento__sum'] - data['t_gastos']['id_movimiento__monto_movimiento__sum']
        data["Diferencia_USD"] = data['t_ingresos_USD']['id_movimiento__monto_movimiento__sum'] - data['t_gastos_USD']['id_movimiento__monto_movimiento__sum']
        data["Diferencia_EUR"] = data['t_ingresos_EUR']['id_movimiento__monto_movimiento__sum'] - data['t_gastos_EUR']['id_movimiento__monto_movimiento__sum']

        data['fecha_generado'] = timezone.now()

        mes = ["", "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE",
               "NOVIEMBRE", "DICIEMBRE"]

        data['mes_cierre'] = mes[int(today.strftime("%m"))]
        data['año_cierre'] = today.strftime("%Y")
        data['datos_condominio'] = datos_condominio
        data['bancos'] = list(Bancos.objects.filter(id_condominio=datos_condominio).order_by('nombre_banco'))

        nombre_pdf = "cierre_mes/{}.pdf".format(today.strftime("%d-%m-%Y_%H.%M.%S"))

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + nombre_pdf + '"'

        template = get_template(template_path)
        html = template.render(data)

        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        if pisa_status.err:
            return HttpResponse('Ha ocurrido al crear el PDF <pre>' + html + '</pre>. Por favor intentelo más tarde.')

        pdf_data = response.getvalue()
        dbb_pdf = Cierre_mes()
        dbb_pdf.fecha_cierre = today
        dbb_pdf.pdf_cierre.save(response.get('Content-Disposition').split('filename="')[1].replace('"', ''),
                                ContentFile(pdf_data))
        dbb_pdf.id_condominio = datos_condominio
        dbb_pdf.save()

        resultado = resultado_gasto.aggregate(Sum('id_movimiento__monto_movimiento'))
        gasto_total = resultado.get('id_movimiento__monto_movimiento__sum') or Decimal('0')

        resultado = resultado_ingreso.aggregate(Sum('id_movimiento__monto_movimiento'))
        ingreso_total = resultado.get('id_movimiento__monto_movimiento__sum') or Decimal('0')

        # Gastos del condominio a repartir = gastos período + fondos − ingresos período
        gastos_a_repartir = gasto_total + Decimal(str(total_fondos)) - ingreso_total

        cuota_mensual = Cuota_mensual()
        cuota_mensual.fecha_publicacion = today.strftime("%Y-%m-%d")
        cuota_mensual.monto_cuota = gastos_a_repartir
        cuota_mensual.id_condominio = datos_condominio
        cuota_mensual.mes = mes[int(today.strftime("%m"))]
        cuota_mensual.save()

        # Solo domicilios de este condominio
        domicilios_qs = Domicilio.objects.filter(id_condominio=datos_condominio)
        # Total m²: si el condominio tiene superficie total definida, usarla; si no, suma de m² de domicilios
        if getattr(datos_condominio, 'superficie_total_m2', None) is not None and datos_condominio.superficie_total_m2 > 0:
            total_m2 = datos_condominio.superficie_total_m2
        else:
            total_m2 = Decimal('0')
            for d in domicilios_qs:
                try:
                    val = d.size_domicilio
                    if val is not None and str(val).strip():
                        total_m2 += Decimal(str(val).replace(',', '.'))
                except (TypeError, ValueError):
                    pass

        # Desactivar deudas CONDOMINIO anteriores de este condominio (no se borran; solo dejan de mostrarse en pagos)
        ids_domicilios = [dom.id_domicilio for dom in domicilios_qs]
        Deudas.objects.filter(
            categoria_deuda="CONDOMINIO",
            tipo_deuda="2",
            id_domicilio_id__in=ids_domicilios,
            is_active=True,
        ).update(is_active=False)

        for dom in domicilios_qs:
            deudas_prop = Deudas()
            deudor = Domicilio.objects.get(id_domicilio=dom.id_domicilio)

            # Prioridad: usar la alícuota que ya tiene la administración; si no hay, derivar de m²
            try:
                m2_dom = Decimal(str(dom.size_domicilio).replace(',', '.')) if dom.size_domicilio else Decimal('0')
            except (TypeError, ValueError):
                m2_dom = Decimal('0')

            if dom.alicuota_domicilio is not None:
                a = float(dom.alicuota_domicilio)
                alicuota_decimal = (a / 100) if a > 1 else a
            elif total_m2 and total_m2 > 0 and m2_dom > 0:
                alicuota_decimal = float(m2_dom / total_m2)
                # Asignar al inmueble para que el propietario la vea y quede para futuros cierres
                Domicilio.objects.filter(id_domicilio=dom.id_domicilio).update(alicuota_domicilio=alicuota_decimal)
            else:
                alicuota_decimal = 0

            # Deuda del inmueble = Gastos a repartir × Alícuota
            monto_deuda = gastos_a_repartir * Decimal(str(alicuota_decimal))

            deudas_prop.fecha_deuda = today.strftime("%Y-%m-%d")
            deudas_prop.tipo_deuda = "2"
            deudas_prop.categoria_deuda = "CONDOMINIO"
            deudas_prop.monto_deuda = monto_deuda
            deudas_prop.tipo_moneda = "BS"
            deudas_prop.is_active = True
            deudas_prop.created_at = today
            deudas_prop.updated_at = today
            deudas_prop.id_domicilio = deudor
            deudas_prop.id_condominio = datos_condominio
            deudas_prop.concepto_deuda = "CONDOMINIO"
            deudas_prop.descripcion_deuda = "CONDOMINIO " + mes[int(today.strftime("%m"))] + " DE " + str(today.strftime("%Y"))
            deudas_prop.save()

            if monto_deuda > 0:
                Domicilio.objects.filter(id_domicilio=deudor.id_domicilio).update(estado_deuda=True)

        return response

    total_ingresos_bs = resultado_ingreso.filter(
        id_movimiento__tipo_moneda__iexact="BS"
    ).aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0
    total_ingresos_usd = resultado_ingreso.filter(
        id_movimiento__tipo_moneda__iexact="USD"
    ).aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0
    total_ingresos_eur = resultado_ingreso.filter(
        id_movimiento__tipo_moneda__iexact="EUR"
    ).aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0
    total_gastos_bs = resultado_gasto.filter(
        id_movimiento__tipo_moneda__iexact="BS"
    ).aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0
    total_gastos_usd = resultado_gasto.filter(
        id_movimiento__tipo_moneda__iexact="USD"
    ).aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0
    total_gastos_eur = resultado_gasto.filter(
        id_movimiento__tipo_moneda__iexact="EUR"
    ).aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0

    # Monto total de las deudas activas (para la barra amarilla del cuadro 2)
    total_monto_deudas = deudas.aggregate(Sum('monto_deuda'))['monto_deuda__sum'] or 0

    return render(request, 'administrador/cierre.html', {'conf': condominio,
                                                         'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro, 'gasto_monto': g_monto,
                                                         'ingreso_monto': i_monto, 'resultado_ingreso': resultado_ingreso,
                                                         'resultado_gasto': resultado_gasto, 'resultado_fondo': resultado_fondo,
                                                         'meses_graficos': mes_final, 'deudas': deudas,
                                                         'deudas_prop': deudas_prop,
                                                         'total_ingresos_bs': total_ingresos_bs,
                                                         'total_ingresos_usd': total_ingresos_usd,
                                                         'total_ingresos_eur': total_ingresos_eur,
                                                         'total_gastos_bs': total_gastos_bs,
                                                         'total_gastos_usd': total_gastos_usd,
                                                         'total_gastos_eur': total_gastos_eur,
                                                         'total_monto_deudas': total_monto_deudas})


def _build_cierre_preview_data(user, resultado_ingreso, resultado_gasto, movimientos_propietarios,
                               tasa_bs, tasa_euro, today, resultado_fondo, ultimo_cierre=None):
    """Construye el diccionario de datos para el PDF de cierre o la vista precierre (sin guardar nada)."""
    datos_condominio = Condominio.objects.filter(id_condominio=user.id_condominio_id).first()
    if not datos_condominio:
        return None
    ingreso_ids = resultado_ingreso.values_list('id_movimiento_id', flat=True)
    movimientos_propietarios = movimientos_propietarios.exclude(id_movimiento__in=ingreso_ids)

    gastos_lista = []
    for gasto in resultado_gasto:
        _d = (gasto.id_movimiento.descripcion_movimiento or gasto.id_movimiento.concepto_movimiento or '')
        if gasto.id_movimiento.tipo_moneda == "BS":
            gastos_lista.append({'descripcion': _d, 'monto': gasto.id_movimiento.monto_movimiento})
        elif gasto.id_movimiento.tipo_moneda == "USD":
            gastos_lista.append({'descripcion': _d, 'monto': Decimal(gasto.id_movimiento.monto_movimiento) / Decimal(tasa_bs)})
        elif gasto.id_movimiento.tipo_moneda == "EUR":
            gastos_lista.append({'descripcion': _d, 'monto': Decimal(gasto.id_movimiento.monto_movimiento) / Decimal(tasa_euro)})

    ingresos_lista = []
    for ingreso in resultado_ingreso:
        _d = (ingreso.id_movimiento.descripcion_movimiento or ingreso.id_movimiento.concepto_movimiento or '')
        if ingreso.id_movimiento.tipo_moneda == "BS":
            ingresos_lista.append({'descripcion': _d, 'monto': ingreso.id_movimiento.monto_movimiento})
        elif ingreso.id_movimiento.tipo_moneda == "USD":
            ingresos_lista.append({'descripcion': _d, 'monto': Decimal(ingreso.id_movimiento.monto_movimiento) / Decimal(tasa_bs)})
        elif ingreso.id_movimiento.tipo_moneda == "EUR":
            ingresos_lista.append({'descripcion': _d, 'monto': Decimal(ingreso.id_movimiento.monto_movimiento) / Decimal(tasa_euro)})
    for mov_prop in movimientos_propietarios:
        _d = (mov_prop.descripcion_movimiento or mov_prop.concepto_movimiento or '')
        if mov_prop.tipo_moneda == "BS":
            ingresos_lista.append({'descripcion': _d, 'monto': mov_prop.monto_movimiento})
        elif mov_prop.tipo_moneda == "USD":
            ingresos_lista.append({'descripcion': _d, 'monto': Decimal(mov_prop.monto_movimiento) / Decimal(tasa_bs)})
        elif mov_prop.tipo_moneda == "EUR":
            ingresos_lista.append({'descripcion': _d, 'monto': Decimal(mov_prop.monto_movimiento) / Decimal(tasa_euro)})

    total_ingresos_bs = resultado_ingreso.filter(id_movimiento__tipo_moneda__iexact="BS").aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0
    total_ingresos_usd = resultado_ingreso.filter(id_movimiento__tipo_moneda__iexact="USD").aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0
    total_ingresos_eur = resultado_ingreso.filter(id_movimiento__tipo_moneda__iexact="EUR").aggregate(Sum('id_movimiento__monto_movimiento'))['id_movimiento__monto_movimiento__sum'] or 0
    total_mov_prop_bs = movimientos_propietarios.filter(tipo_moneda__iexact="BS").aggregate(Sum('monto_movimiento'))['monto_movimiento__sum'] or 0
    total_mov_prop_usd = movimientos_propietarios.filter(tipo_moneda__iexact="USD").aggregate(Sum('monto_movimiento'))['monto_movimiento__sum'] or 0
    total_mov_prop_eur = movimientos_propietarios.filter(tipo_moneda__iexact="EUR").aggregate(Sum('monto_movimiento'))['monto_movimiento__sum'] or 0

    data = {
        'gastos': gastos_lista,
        'ingresos': ingresos_lista,
        't_gastos': resultado_gasto.filter(id_movimiento__tipo_moneda__iexact="BS").aggregate(Sum('id_movimiento__monto_movimiento')),
        't_gastos_USD': resultado_gasto.filter(id_movimiento__tipo_moneda__iexact="USD").aggregate(Sum('id_movimiento__monto_movimiento')),
        't_gastos_EUR': resultado_gasto.filter(id_movimiento__tipo_moneda__iexact="EUR").aggregate(Sum('id_movimiento__monto_movimiento')),
        't_ingresos': {'id_movimiento__monto_movimiento__sum': total_ingresos_bs + total_mov_prop_bs},
        't_ingresos_USD': {'id_movimiento__monto_movimiento__sum': total_ingresos_usd + total_mov_prop_usd},
        't_ingresos_EUR': {'id_movimiento__monto_movimiento__sum': total_ingresos_eur + total_mov_prop_eur},
    }

    if Precios.objects.exists():
        precios = Precios.objects.all().last()
        precio = [precios.maleteros, precios.salon_fiesta, precios.otras_areas]
    else:
        precio = [0, 0, 0]
    tipo_precio = ["Maleteros", "Mantenimiento de Áreas", "Mantenimiento del Edificio", "Jardinería"]
    data['precios'] = zip(precio, tipo_precio)

    if Recargos_y_Descuentos.objects.filter(id_condominio=datos_condominio).exists():
        recargos_descuentos = Recargos_y_Descuentos.objects.filter(id_condominio=datos_condominio).last()
        recargo_descuento = [str(recargos_descuentos.recargo_moratorio) + "%", recargos_descuentos.dia_recargo,
                             str(recargos_descuentos.descuento_pronto_pago) + "%", recargos_descuentos.dia_descuento]
    else:
        recargo_descuento = ["0%", 1, "0%", 1]
    tipo_recargo_descuento = ["Recargo por morosidad", "Dia de aplicación de la mororsidad", "Descuento por pronto pago", "Dia de finalización del descuento"]
    data['recargos_descuentos'] = zip(recargo_descuento, tipo_recargo_descuento)

    monto_deuda_condo = Deudas.objects.filter(is_active=True, tipo_deuda="1").aggregate(Sum('monto_deuda'))['monto_deuda__sum'] or 0
    monto_deuda_prop = Deudas.objects.filter(is_active=True, tipo_deuda="2", id_domicilio__id_condominio=datos_condominio).aggregate(Sum('monto_deuda'))['monto_deuda__sum'] or 0
    data['monto_deuda_condo'] = monto_deuda_condo
    data['monto_deuda_prop'] = monto_deuda_prop
    data['t_deudas'] = monto_deuda_condo + monto_deuda_prop

    filtro_fondos_condo = {'id_movimiento__id_banco__id_condominio_id': user.id_condominio_id}
    fondo_reserva = Fondos.objects.filter(tipo_fondo="RESERVA", **filtro_fondos_condo).aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
    fondo_operacional = Fondos.objects.filter(tipo_fondo="OPERACIONAL", **filtro_fondos_condo).aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
    fondo_prestaciones = Fondos.objects.filter(tipo_fondo="PRESTACIONES", **filtro_fondos_condo).aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
    fondo_otros = Fondos.objects.filter(tipo_fondo="OTROS FONDOS", **filtro_fondos_condo).aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
    data['fondo_reserva'] = fondo_reserva
    data['fondo_operacional'] = fondo_operacional
    data['fondo_prestaciones'] = fondo_prestaciones
    data['fondo_otros'] = fondo_otros
    total_fondos = fondo_reserva + fondo_operacional + fondo_prestaciones + fondo_otros

    # Nivel 1: apartado reserva (10% gastos), saldos anteriores, gastos bancarios
    t_g = data['t_gastos']['id_movimiento__monto_movimiento__sum'] or 0
    t_g_usd = data['t_gastos_USD']['id_movimiento__monto_movimiento__sum'] or 0
    t_g_eur = data['t_gastos_EUR']['id_movimiento__monto_movimiento__sum'] or 0
    total_gastos_mes_bs = Decimal(str(t_g)) + Decimal(str(t_g_usd)) / Decimal(str(tasa_bs)) + Decimal(str(t_g_eur)) / Decimal(str(tasa_euro))
    data['apartado_fondo_reserva'] = (total_gastos_mes_bs * Decimal('0.10')).quantize(Decimal('0.01'))
    if ultimo_cierre:
        saldo_ant_reserva = Fondos.objects.filter(
            tipo_fondo="RESERVA", **filtro_fondos_condo,
            id_movimiento__created_at__lte=ultimo_cierre.fecha_cierre
        ).aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
        saldo_ant_prestaciones = Fondos.objects.filter(
            tipo_fondo="PRESTACIONES", **filtro_fondos_condo,
            id_movimiento__created_at__lte=ultimo_cierre.fecha_cierre
        ).aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
        gastos_bancarios_bs = Gastos.objects.filter(
            tipo_gasto='GASTOS BANCARIOS',
            id_movimiento__created_at__gt=ultimo_cierre.fecha_cierre,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).aggregate(total=Sum('id_movimiento__monto_movimiento'))['total'] or 0
    else:
        saldo_ant_reserva = Decimal('0')
        saldo_ant_prestaciones = Decimal('0')
        gastos_bancarios_bs = 0
    data['saldo_anterior_reserva'] = saldo_ant_reserva
    data['saldo_anterior_prestaciones'] = saldo_ant_prestaciones
    data['saldo_actual_reserva'] = (Decimal(str(saldo_ant_reserva)) + data['apartado_fondo_reserva']).quantize(Decimal('0.01'))
    data['apartado_prestaciones'] = Decimal('0')
    data['saldo_actual_prestaciones'] = saldo_ant_prestaciones
    data['total_gastos_bancarios_mes'] = gastos_bancarios_bs

    t_g = data['t_gastos']['id_movimiento__monto_movimiento__sum'] or 0
    t_i = data['t_ingresos']['id_movimiento__monto_movimiento__sum'] or 0
    t_g_usd = data['t_gastos_USD']['id_movimiento__monto_movimiento__sum'] or 0
    t_i_usd = data['t_ingresos_USD']['id_movimiento__monto_movimiento__sum'] or 0
    t_g_eur = data['t_gastos_EUR']['id_movimiento__monto_movimiento__sum'] or 0
    t_i_eur = data['t_ingresos_EUR']['id_movimiento__monto_movimiento__sum'] or 0
    data["Diferencia"] = t_i - t_g
    data["Diferencia_USD"] = t_i_usd - t_g_usd
    data["Diferencia_EUR"] = t_i_eur - t_g_eur
    data['fecha_generado'] = today
    mes = ["", "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    data['mes_cierre'] = mes[int(today.strftime("%m"))]
    data['año_cierre'] = today.strftime("%Y")
    data['datos_condominio'] = datos_condominio
    return data


@login_required
def precierre(request):
    """Vista previa del cierre del mes: mismos datos que el cierre pero sin ejecutarlo."""
    user = request.user
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.filter(id_condominio=user.id_condominio_id)
    datos_condominio = condominio.first()
    if not datos_condominio:
        messages.warning(request, 'No hay condominio configurado.', extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:admin_cierres'))

    ultima_tasa = Tasas.objects.last()
    if not ultima_tasa:
        messages.warning(request, 'Configure las tasas antes de ver el precierre.', extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:admin_cierres'))

    today = timezone.now()
    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR
    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)
    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    cierre_mes = Cierre_mes.objects.filter(id_condominio_id=user.id_condominio_id)
    if cierre_mes.exists():
        ultimo_cierre = cierre_mes.last()
        resultado_ingreso = Ingresos.objects.filter(
            id_movimiento__created_at__gt=ultimo_cierre.fecha_cierre,
            id_movimiento__estado_movimiento=0,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento")
        movimientos_propietarios = Movimientos_bancarios.objects.filter(
            estado_movimiento=0,
            id_banco__id_condominio_id=user.id_condominio_id,
            created_at__gt=ultimo_cierre.fecha_cierre,
        ).select_related("id_banco")
        resultado_gasto = Gastos.objects.filter(
            id_movimiento__created_at__gt=ultimo_cierre.fecha_cierre,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento")
        resultado_fondo = Fondos.objects.filter(
            id_movimiento__created_at__gt=ultimo_cierre.fecha_cierre,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento")
    else:
        filtro_condo = {'id_movimiento__id_banco__id_condominio_id': user.id_condominio_id}
        ingresos = Ingresos.objects.filter(**filtro_condo).first()
        gastos = Gastos.objects.filter(**filtro_condo).first()
        fondos = Fondos.objects.filter(**filtro_condo).first()
        resultado_ingreso = Ingresos.objects.filter(
            id_movimiento__created_at__gte=ingresos.id_movimiento.created_at,
            id_movimiento__estado_movimiento=0,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento") if ingresos else Ingresos.objects.none()
        movimientos_propietarios = Movimientos_bancarios.objects.filter(
            estado_movimiento=0,
            id_banco__id_condominio_id=user.id_condominio_id,
            created_at__gte=ingresos.id_movimiento.created_at,
        ).select_related("id_banco") if ingresos else Movimientos_bancarios.objects.none()
        resultado_gasto = Gastos.objects.filter(
            id_movimiento__created_at__gte=gastos.id_movimiento.created_at,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento") if gastos else Gastos.objects.none()
        resultado_fondo = Fondos.objects.filter(
            id_movimiento__created_at__gte=fondos.id_movimiento.created_at,
            id_movimiento__id_banco__id_condominio_id=user.id_condominio_id,
        ).select_related("id_movimiento") if fondos else Fondos.objects.none()

    ultimo_cierre = cierre_mes.last() if cierre_mes.exists() else None
    data = _build_cierre_preview_data(user, resultado_ingreso, resultado_gasto, movimientos_propietarios, tasa_bs, tasa_euro, today, resultado_fondo, ultimo_cierre=ultimo_cierre)
    if not data:
        return HttpResponseRedirect(reverse('condominio_app:admin_cierres'))

    bancos = Bancos.objects.filter(id_condominio=datos_condominio).order_by('nombre_banco')
    data['bancos_cabecera'] = bancos
    data['es_precierre'] = True
    return render(request, 'administrador/precierre.html', data)


@login_required
def cierre_propietario(request, prop, cierre, user):

    # Obtener la consulta anterior
    cierre_anterior = Cierre_mes.objects.filter(id_cierre__lt=cierre.id_cierre).last()

    if cierre_anterior:

        template_path = 'PDF/cierre_mes_propietario.html'
        data = {}

        data['fecha_generado'] = timezone.now()

        mes = ["", "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE",
               "NOVIEMBRE", "DICIEMBRE"]

        data['mes_cierre'] = mes[int(cierre.fecha_cierre.strftime("%m"))]
        data['año_cierre'] = cierre.fecha_cierre.strftime("%Y")

        movimientos_ids = Ingresos.objects.filter(id_propietario_id=prop.id_propietario).values_list('id_movimiento_id', flat=True)
        data['movimientos'] = Movimientos_bancarios.objects.filter(pk__in=movimientos_ids, estado_movimiento=0, id_banco__id_condominio_id=user.id_condominio_id, created_at__range=[cierre_anterior.fecha_cierre, cierre.fecha_cierre]).select_related('id_banco')
        data['deudas'] = Deudas.objects.filter(tipo_deuda="2", id_domicilio__id_propietario__id_usuario__id_condominio_id=user.id_condominio_id, is_active=True).select_related('id_domicilio')
        data['datos_propietario'] = prop
        data['datos_condominio'] = Condominio.objects.get(id_condominio=request.user.id_condominio_id)
        data['datos_domicilio'] = Domicilio.objects.filter(id_propietario_id=prop.id_propietario)
        todos_bancos = Bancos.objects.filter(id_condominio_id=request.user.id_condominio_id)
        nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
        data['bancos_cabecera'] = [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in todos_bancos]

        nombre_pdf = "cierre_mes_{}_{}.pdf".format(prop.nombre_propietario, cierre.fecha_cierre.strftime("%d-%m-%Y %H.%M.%S"))

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + nombre_pdf + '"'

        template = get_template(template_path)
        html = template.render(data)

        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        if pisa_status.err:
            return HttpResponse('Ha ocurrido al crear el PDF <pre>' + html + '</pre>. Por favor intentelo más tarde.')

        return response

    else:

        template_path = 'PDF/cierre_mes_propietario.html'
        data = {}

        data['fecha_generado'] = timezone.now()

        mes = ["", "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE",
               "NOVIEMBRE", "DICIEMBRE"]

        data['mes_cierre'] = mes[int(cierre.fecha_cierre.strftime("%m"))]
        data['año_cierre'] = cierre.fecha_cierre.strftime("%Y")

        movimientos_ids = Ingresos.objects.filter(id_propietario_id=prop.id_propietario).values_list('id_movimiento_id', flat=True)
        data['movimientos'] = Movimientos_bancarios.objects.filter(pk__in=movimientos_ids, estado_movimiento=0, id_banco__id_condominio_id=user.id_condominio_id, created_at__lte=cierre.fecha_cierre)
        data['deudas'] = Deudas.objects.filter(tipo_deuda="2", id_domicilio__id_propietario__id_usuario__id_condominio_id=user.id_condominio_id, is_active=True).select_related('id_domicilio')
        data['datos_propietario'] = prop.select_related('id_usuario')
        data['datos_condominio'] = Condominio.objects.get(id_condominio=request.user.id_condominio_id)
        data['datos_domicilio'] = Domicilio.objects.filter(id_propietario_id=prop.id_propietario)
        todos_bancos = Bancos.objects.filter(id_condominio_id=request.user.id_condominio_id)
        nro_cuenta_fmt = lambda n: ' '.join((n or '')[i:i+4] for i in range(0, len(n or ''), 4)) if n else ''
        data['bancos_cabecera'] = [{'nombre_banco': b.nombre_banco, 'nro_cuenta_formateado': nro_cuenta_fmt(b.nro_cuenta)} for b in todos_bancos]

        nombre_pdf = "cierre_mes_{}_{}.pdf".format(prop.nombre_propietario, cierre.fecha_cierre.strftime("%d-%m-%Y %H.%M.%S"))

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + nombre_pdf + '"'

        template = get_template(template_path)
        html = template.render(data)

        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        if pisa_status.err:
            return HttpResponse('Ha ocurrido al crear el PDF <pre>' + html + '</pre>. Por favor intentelo más tarde.')

        return response

# ------------------------------ADMINISTRACION Y GESTIÓN DE NOTICIAS------------------------------
@login_required
def admin_noticias(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    post_form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    noticias = Noticia.objects.filter(id_condominio_id=user.id_condominio_id).order_by('-fecha_actualizado')
    ultima_tasa = Tasas.objects.all().last()
    if not ultima_tasa:
        messages.warning(request, 'Configure las tasas de cambio en Configuración antes de usar este módulo.', extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': 'tasa'}))
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        if post_form.is_valid():

            obj = post_form.save(commit=False)
            obj.id_condominio_id = user.id_condominio_id
            autor = Usuario.objects.filter(email=request.user.email).first()
            obj.autor = autor
            obj.save()
            post_form = CreateBlogPostForm()
            messages.success(request, '¡La noticia o comunicado se ha publicado de manera satisfactoria!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_noticias'))
        else:
            messages.warning(request,
                             'Ha ocurrido un error al publicar la noticia o comunicado. Por favor verifique e intente de nuevo.',
                             extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:admin_noticias'))

    return render(request, 'administrador/noticias.html', {'post_form': post_form, 'noticias': noticias,
                                                           'conf': condominio, 'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro})


# ------------------------------PERFIL------------------------------
@login_required
def admin_perfil(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    return render(request, 'administrador/perfil.html', {'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro})


# ------------------------------TORRES------------------------------
@login_required
def admin_torres(request):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    torres = Torre.objects.all()
    torre_form = TorreForm()
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':

        torre_form = TorreForm(data=request.POST)

        if torre_form.is_valid():
            torre = torre_form.save()
            torre.id_condominio = condominio
            torre.save()
            messages.success(request, '¡La torre ha sido registrada con exito!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "torres"}))

        else:
            messages.warning(request,
                             'Ha ocurrido un error al registrar la torre. Por favor verifique e intente de nuevo.',
                             extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "torres"}))

    return render(request, 'administrador/torres.html', {'conf': condominio, 'tasa_bs': tasa_bs,
                                                         'tasa_euro': tasa_euro, 'torres_form': torre_form, 'torres': torres})


# ------------------------------READ VIEWS------------------------------
@login_required
def readBancos(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    bancos = Bancos.objects.filter(id_banco=id).first()
    if not bancos:
        messages.warning(request, 'El banco solicitado no existe o ya fue eliminado.', extra_tags='alert-warning')
        return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "bancos"}))
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    return render(request, 'administrador/read/bancos_read.html', {
        'bancos': bancos,
        'conf': condominio,
        'tasa_bs': tasa_bs,
        'tasa_euro': tasa_euro,
        'back_url': reverse('condominio_app:admin_configuracion', kwargs={'type': "condominio"}) + '?tab=bancos&lista=1',
    })


@login_required
def readGastos(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    gastos = Gastos.objects.select_related("id_movimiento__id_banco").get(id_gasto=id)

    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    return render(request, 'administrador/read/gastos_read.html', {
        'gastos': gastos,
        'conf': condominio,
        'tasa_bs': tasa_bs,
        'tasa_euro': tasa_euro,
        'back_url': reverse('condominio_app:admin_gastos').rstrip('/') + '?lista=1',
    })


@login_required
def readIngresos(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    ingresos = Ingresos.objects.select_related("id_movimiento__id_banco").get(id_ingreso=id)
    propietario = Propietario.objects.filter(id_propietario=ingresos.id_propietario_id)

    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    return render(request, 'administrador/read/ingresos_read.html', {
        'ingresos': ingresos,
        'conf': condominio,
        'propietario': propietario,
        'tasa_bs': tasa_bs,
        'tasa_euro': tasa_euro,
        'back_url': reverse('condominio_app:admin_ingresos') + '?lista=1',
    })

@login_required
def readPagoMovimiento(request, id):
    user = request.user
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    mov = Movimientos_bancarios.objects.select_related('id_banco').filter(
        id_movimiento=id,
        id_banco__id_condominio_id=user.id_condominio_id
    ).first()
    if not mov:
        messages.warning(request, 'No se encontró el pago solicitado.', extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:admin_propietarios'))

    datos_mov = Datos_transaccion.objects.filter(id_movimiento_id=mov.id_movimiento).first()
    ingreso = Ingresos.objects.filter(id_movimiento_id=mov.id_movimiento).select_related('id_propietario').first()
    recibos = Recibos.objects.filter(id_movimiento_id=mov.id_movimiento).select_related('id_deuda').all()

    propietario = None
    if ingreso and ingreso.id_propietario:
        propietario = ingreso.id_propietario
    elif recibos:
        first_recibo = recibos.first()
        if first_recibo.id_deuda and first_recibo.id_deuda.id_domicilio:
            propietario = first_recibo.id_deuda.id_domicilio.id_propietario

    return render(
        request,
        'administrador/read/pagos_read.html',
        {
            'movimiento': mov,
            'datos_mov': datos_mov,
            'ingreso': ingreso,
            'recibos': recibos,
            'propietario': propietario,
            'back_url': get_back_url(request, reverse('condominio_app:admin_validacion_pagos')),
        }
    )

@login_required
def readDeudas(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    deuda_condo = Deudas.objects.filter(id_deuda=id, tipo_deuda="1")
    deuda_prop = Deudas.objects.filter(id_deuda=id, tipo_deuda="2")
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if deuda_condo.exists():
        deudas = deuda_condo
    else:
        deudas = deuda_prop

    return render(request, 'administrador/read/deudas_read.html', {
        'deudas': deudas,
        'conf': condominio,
        'tasa_bs': tasa_bs,
        'tasa_euro': tasa_euro,
        'back_url': get_back_url(request, reverse('condominio_app:admin_deudas')),
    })


def readPropDeudas(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    deudas_prop = Deudas.objects.filter(id_domicilio=id).select_related('id_domicilio__id_propietario')
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    return render(request, 'administrador/read/deudas_prop_read.html', {
        'deudas_prop': deudas_prop,
        'conf': condominio,
        'tasa_bs': tasa_bs,
        'tasa_euro': tasa_euro,
        'back_url': get_back_url(request, reverse('condominio_app:admin_deudas')),
    })


@login_required
def readPropietarios(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    prop = Propietario.objects.select_related('id_usuario').get(id_propietario=id)
    print(prop.genero)
    domicilios = Domicilio.objects.filter(id_propietario=id).values_list('nombre_domicilio', flat=True)
    dom = Domicilio.objects.filter(id_propietario_id=id)
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    back_fallback = reverse('condominio_app:admin_configuracion', kwargs={'type': 'condominio'}) + '?tab=propietarios'
    back_url = get_back_url(request, back_fallback)
    if request.GET.get('back') == 'propietarios':
        back_url = back_fallback
    return render(request, 'administrador/read/propietario_read.html', {'prop': prop, 'domicilios': domicilios, 'dom': dom, 'conf': condominio,
                                                                        'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro,
                                                                        'back_url': back_url})


@login_required
def readCuentas(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    usuarios = Usuario.objects.get(id=id)
    propietarios = usuarios.id_propietario
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()
    print(propietarios)
    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    return render(request, 'administrador/read/cuentas_read.html', {
        'propietarios': propietarios,
        'usuarios': usuarios,
        'conf': condominio,
        'tasa_bs': tasa_bs,
        'tasa_euro': tasa_euro,
        'back_url': get_back_url(request, reverse('condominio_app:admin_cuentas')),
    })


# ------------------------------UPDATE VIEWS------------------------------
@login_required
def updateBancos(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    bancos = Bancos.objects.get(id_banco=id)
    bancos_form = BancosForm()
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']
    
    tlf_titular = bancos.tlf_titular or ""
    partes_tlf = tlf_titular.split('-', 1)
    if len(partes_tlf) == 2:
        codigo = partes_tlf[0]
        tlf = partes_tlf[1]
    else:
        codigo = ""
        tlf = partes_tlf[0]

    cod_tlf = BancosForm(initial={'cod_tlf': codigo})
    tipo_moneda = BancosForm(initial={'tipo_moneda': bancos.tipo_moneda})

    if request.method == 'POST':

        dataBanco = {
            'tipo_moneda': bancos.tipo_moneda,
            'nombre_titular': request.POST['nombre_titular'],
            'tipo_dni_titular': request.POST['tipo_dni_titular'],
            'dni_titular': request.POST['dni_titular'],
            'nombre_banco': bancos.nombre_banco,
            'nro_cuenta': request.POST['nro_cuenta'],
            'email_titular': request.POST['email_titular'],
            'tlf_titular': str(request.POST['cod_tlf'])+"-"+str(request.POST['tlf_titular']),
            'saldo_actual': bancos.saldo_actual,
            'fecha_apertura': bancos.fecha_apertura,
            'tipo_banco': bancos.tipo_banco
        }

        bancos_form = BancosForm(data=dataBanco, instance=bancos)

        if bancos_form.is_valid():

            Bancos.objects.filter(pk=id).update(nombre_titular=request.POST['nombre_titular'],
                                                tipo_dni_titular=request.POST['tipo_dni_titular'],
                                                dni_titular=request.POST['dni_titular'],
                                                nro_cuenta=request.POST['nro_cuenta'],
                                                email_titular=request.POST['email_titular'],
                                                tlf_titular=str(request.POST['cod_tlf'])+"-"+str(request.POST['tlf_titular']),
                                                updated_at=today)
            if request.FILES.get('imagen_referencial'):
                bancos.imagen_referencial = request.FILES['imagen_referencial']
                bancos.save()

            messages.success(request, '¡El banco ha sido actualizado de manera satisfactoria!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "bancos"}))
        else:
            print(bancos_form.errors)
            primera_key = next(iter(bancos_form.errors))
            messages.warning(request,
                             bancos_form.errors[primera_key].as_text().replace('*', ''),
                             extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "bancos"}))

    return render(request, 'administrador/update/bancos_update.html', {'bancos': bancos, 'bancos_form': bancos_form,
                                                                       'conf': condominio, 'tasa_bs': tasa_bs,
                                                                       'tasa_euro': tasa_euro, 'tipo_moneda':tipo_moneda,
                                                                       'tlf': tlf, 'cod_tlf': cod_tlf})


@login_required
def updateGastos(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    gastos = Gastos.objects.select_related("id_movimiento").get(id_gasto=id)
    datos_mov = Datos_transaccion.objects.get(id_movimiento_id=gastos.id_movimiento_id)
    cierre = Cierre_mes.objects.filter(id_condominio_id=user.id_condominio_id).order_by('fecha_cierre').last()
    if cierre and gastos.id_movimiento.fecha_movimiento:
        cierre_date = cierre.fecha_cierre.date()
        fecha_gasto = gastos.id_movimiento.fecha_movimiento
        mov_created_at = gastos.id_movimiento.created_at
        if (
            fecha_gasto < cierre_date
            or (
                fecha_gasto == cierre_date
                and (not mov_created_at or mov_created_at <= cierre.fecha_cierre)
            )
        ):
            messages.warning(request, 'No puedes modificar un gasto de un mes ya cerrado.', extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:admin_gastos'))

    gastos_form = GastosForm()
    movimientos_form = MovimientoForm()
    datos_mov_form = DatosMovimientoForm() 

    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    identificacion = str(datos_mov.dni_titular).split("-")
    tipo_dni = DatosMovimientoForm(initial={'tipo_dni_titular': identificacion[0]})
    metodo_pago = GastosForm(initial={'metodo_pago': gastos.metodo_pago})

    factura = ""

    if gastos.factura:
        factura = gastos.factura
    else:
        pass

    if request.method == 'POST':

        # Revisamos si la fecha del gasto introducida es mayor a la del día actual, en caso de ser True entonces se arroja un error
        if request.POST['fecha_movimiento'] > str(date.today()):
            messages.warning(request,
                             'Ha ocurrido un error durante la actualización. La fecha del gasto no puede ser mayor a la del día actual',
                             extra_tags='alert-danger')

        else:
            gastos.id_movimiento.concepto_movimiento = (request.POST.get('descripcion_movimiento') or '')[:255]
            gastos.id_movimiento.descripcion_movimiento = request.POST['descripcion_movimiento'].upper()
            gastos.id_movimiento.referencia_movimiento = request.POST['referencia']
            gastos.id_movimiento.fecha_movimiento = request.POST['fecha_movimiento']
            gastos.id_movimiento.save()

            gastos.metodo_pago = request.POST['metodo_pago']

            if 'imgGasto' in request.FILES:
                gastos.concepto_movimiento = (request.POST.get('descripcion_movimiento') or '')[:255]
                gastos.imagen_referencial = request.FILES['imgGasto']

            elif gastos.imagen_referencial:
                gastos.imagen_referencial = gastos.imagen_referencial

            else:
                gastos.imagen_referencial = None

            if request.POST['metodo_pago'] == "0":
                gastos.factura = request.POST['factura']
            else:
                gastos.factura = None

            # Se guarda el registro del gasto actualizado
            gastos.save()

            datos_mov.dni_titular = request.POST['tipo_dni_titular'] + "-" + request.POST['dni_titular']
            datos_mov.save()

            messages.success(request, '¡El gasto ha sido actualizado de manera satisfactoria!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_gastos'))

    return render(request, 'administrador/update/gastos_update.html', {'gastos': gastos, 'gastos_form': gastos_form, 'identificacion': identificacion,
                                                                       'movimientos_form': movimientos_form, 'datos_mov_form': datos_mov_form,
                                                                       'conf': condominio, 'datos_mov': datos_mov, 'factura': factura,
                                                                       'metodo_pago': metodo_pago, 'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro,
                                                                       'tipo_dni': tipo_dni, 'identificacion': identificacion})


@login_required
def updateIngresos(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    condominio = Condominio.objects.get(id_condominio=user.id_condominio_id)
    ingresos = Ingresos.objects.select_related("id_movimiento").get(id_ingreso=id)
    datos_mov = Datos_transaccion.objects.get(id_movimiento_id=ingresos.id_movimiento_id)

    ingresos_form = IngresosForm()
    movimientos_form = MovimientoForm()
    datos_mov_form = DatosMovimientoForm() 

    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    identificacion = str(datos_mov.dni_titular).split("-")
    tipo_dni = DatosMovimientoForm(initial={'tipo_dni_titular': identificacion[0]})
    metodo_pago = IngresosForm(initial={'metodo_pago': ingresos.metodo_pago})

    if request.method == 'POST':

        # Revisamos si la fecha del gasto introducida es mayor a la del día actual, en caso de ser True entonces se arroja un error
        if request.POST['fecha_movimiento'] > str(date.today()):
            messages.warning(request,
                             'Ha ocurrido un error durante la actualización. La fecha del ingreso no puede ser mayor a la del día actual',
                             extra_tags='alert-danger')

        else:
            ingresos.id_movimiento.concepto_movimiento = (request.POST.get('descripcion_movimiento') or '')[:255]
            ingresos.id_movimiento.descripcion_movimiento = request.POST['descripcion_movimiento'].upper()
            ingresos.id_movimiento.referencia_movimiento = request.POST['referencia']
            ingresos.id_movimiento.fecha_movimiento = request.POST['fecha_movimiento']
            ingresos.id_movimiento.save()

            ingresos.metodo_pago = request.POST['metodo_pago']

            if 'imgIngreso' in request.FILES:
                ingresos.concepto_movimiento = (request.POST.get('descripcion_movimiento') or '')[:255]
                ingresos.imagen_referencial = request.FILES['imgIngreso']

            elif ingresos.imagen_referencial:
                ingresos.imagen_referencial = ingresos.imagen_referencial

            else:
                ingresos.imagen_referencial = None

            if request.POST['metodo_pago'] == "0":
                ingresos.factura = request.POST['factura']
            else:
                ingresos.factura = None

            # Se guarda el registro del gasto actualizado
            ingresos.save()

            datos_mov.dni_titular = request.POST['tipo_dni_titular'] + "-" + request.POST['dni_titular']
            datos_mov.save()

            messages.success(request, '¡El ingreso ha sido actualizado de manera satisfactoria!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_ingresos'))

    return render(request, 'administrador/update/ingresos_update.html', {'ingresos': ingresos, 'ingresos_form': ingresos_form,
                                                                         'movimientos_form': movimientos_form,
                                                                         'datos_mov_form': datos_mov_form,'conf': condominio,
                                                                         'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro,
                                                                         'tipo_dni': tipo_dni, 'identificacion': identificacion,
                                                                         'metodo_pago': metodo_pago})


@login_required
def updatePropietarios(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    conf = Condominio.objects.get(id_condominio=user.id_condominio_id)
    propietario = Propietario.objects.select_related('id_usuario').get(id_propietario=id)
    propietarios_form = PropietariosForm()
    user_form = RegistrationForm()
    torres = Torre.objects.filter(id_condominio_id=user.id_condominio_id)
    domicilios_disponibles = Domicilio.objects.filter(
        id_condominio_id=user.id_condominio_id,
        id_propietario_id__isnull=True,
    ).order_by('nombre_domicilio')
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    # Se asigna el id del propietario que se esta actualizando y su número de apartamento para futuro chequeo
    id_propietario_actualizandose = propietario.id_propietario

    country = PropietariosForm(initial={'pais_residencia': propietario.pais_residencia})
    select_country = country

    genero = PropietariosForm(initial={'genero': propietario.genero})
    select_genero = genero

    tipo_doc = PropietariosForm(initial={'tipo_dni': propietario.tipo_dni})
    select_tipo_doc = tipo_doc

    cod_hab = PropietariosForm(initial={'codigo_tlf_hab': propietario.codigo_tlf_hab})
    select_cod_hab = cod_hab

    cod_mov = PropietariosForm(initial={'codigo_tlf_movil': propietario.codigo_tlf_movil})
    select_cod_mov = cod_mov

    if request.method == 'POST':
        if request.POST.get('form_origen') == 'agregar_inmueble':
            seleccionados = request.POST.getlist('domicilio')
            if not seleccionados:
                messages.warning(request,
                                 'Debe seleccionar al menos un inmueble.',
                                 extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('condominio_app:updatePropietarios', kwargs={'id': id}))
            Domicilio.objects.filter(id_domicilio__in=seleccionados).update(id_propietario_id=id)
            messages.success(request,
                             '¡Los inmuebles fueron asignados correctamente!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:updatePropietarios', kwargs={'id': id}))

        # Tipo de documento: debe venir del POST (V, E, P, J, G, R, O)
        tipo_dni_post = (request.POST.get('tipo_dni') or '').strip()
        if not tipo_dni_post:
            messages.warning(request,
                             'Debe escoger un tipo de identificación (Venezolano, RIF, Jurídico, etc.).',
                             extra_tags='alert-danger')
        else:
            dataPropietario = {
                'nombre_propietario': request.POST.get('nombre_propietario', '').upper(),
                'genero': request.POST.get('genero'),
                'pais_residencia': request.POST.get('pais_residencia'),
                'tipo_dni': tipo_dni_post,
                'dni': request.POST.get('dni'),
                'codigo_tlf_hab': request.POST.get('codigo_tlf_hab'),
                'telefono_hab': request.POST.get('telefono_hab'),
                'codigo_tlf_movil': request.POST.get('codigo_tlf_movil'),
                'telefono_movil': request.POST.get('telefono_movil')
            }

            # Se revisa si no se han ingresado un número de teléfono, en caso de ser así se arroja un error
            if (dataPropietario['telefono_hab'] and dataPropietario['telefono_movil']) == '':
                messages.warning(request,
                                 'Ha ocurrido un error durante la actualización. Debe proveer por lo menos un número de teléfono.',
                                 extra_tags='alert-danger')
            else:
                propietarios_form = PropietariosForm(data=dataPropietario)

                # Se chequea si el formulario de los propietarios es valido
                if propietarios_form.is_valid():
                    # Se chequea si el formulario de los usuarios es valido
                    Propietario.objects.filter(pk=id).update(nombre_propietario=dataPropietario['nombre_propietario'],
                                                             genero=dataPropietario['genero'], pais_residencia=dataPropietario['pais_residencia'],
                                                             tipo_dni=dataPropietario['tipo_dni'], dni=dataPropietario['dni'],
                                                             codigo_tlf_hab=dataPropietario['codigo_tlf_hab'],
                                                             telefono_hab=dataPropietario['telefono_hab'],
                                                             codigo_tlf_movil=dataPropietario['codigo_tlf_movil'],
                                                             telefono_movil=dataPropietario['telefono_movil'])

                    propietario.id_usuario.email = request.POST['email']
                    propietario.id_usuario.save()

                    messages.success(request,
                                     '¡El propietario ha sido actualizado de manera satisfactoria!',
                                     extra_tags='alert-success')
                    return HttpResponseRedirect(reverse('condominio_app:admin_propietarios'))

                else:
                    primera_key = next(iter(propietarios_form.errors))
                    print(propietarios_form.errors)
                    print(iter(propietarios_form.errors))
                    print(next(iter(propietarios_form.errors)))
                    messages.warning(request,
                             propietarios_form.errors.as_text().replace('*', ''),
                             extra_tags='alert-danger')
                    messages.warning(request,
                             propietarios_form.errors[primera_key].as_text().replace('*', ''),
                             extra_tags='alert-danger')

    return render(request, 'administrador/update/propietarios_update.html', {'propietarios_form': propietarios_form, 'user_form': user_form,
                                                                            'propietarios': propietario, 'conf': conf,
                                                                            'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro,
                                                                            'select_country': select_country,
                                                                            'select_genero': select_genero,
                                                                            'select_tipo_doc': select_tipo_doc,
                                                                            'select_cod_hab': select_cod_hab,
                                                                            'select_cod_mov': select_cod_mov,
                                                                            'torres': torres,
                                                                            'domicilios_disponibles': domicilios_disponibles})


class DeudasUpdateView(UpdateView):
    model = Deudas
    form_class = DeudasUpdateForm
    template_name = 'administrador/update/deudas_update.html'
    success_url = reverse_lazy('condominio_app:admin_deudas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conf'] = Condominio.objects.get(id_condominio=self.request.user.id_condominio_id)
        context['tasa_bs'] = Tasas.objects.last().tasa_BCV_USD
        context['tasa_euro'] = Tasas.objects.last().tasa_BCV_EUR
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        messages.success(self.request, '¡La deuda fue modificada con exito!', extra_tags='alert-success')
        return reverse(viewname='condominio_app:admin_deudas')


@login_required
def updateTorres(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    conf = Condominio.objects.get(id_condominio=user.id_condominio_id)
    torre = Torre.objects.get(id_torre=id)
    torre_form = TorreForm()
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':

        torre.nombre_torre = request.POST['nombre_torre']
        torre.pisos = torre.pisos
        torre.id_condominio = conf
        torre.save()
        messages.success(request, '¡La torre ha sido actualizada exitosamente!',
                         extra_tags='alert-success')
        return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "torres"}))

    return render(request, 'administrador/update/torres_update.html', {'conf': conf, 'tasa_bs': tasa_bs,
                                                                         'tasa_euro': tasa_euro, 'torre': torre,
                                                                       'torres_form': torre_form})


@login_required
def updateCuentas(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    conf = Condominio.objects.all()
    usuarios = Usuario.objects.get(id=id)
    propietarios = Propietario.objects.get(id_usuario_id=usuarios.id)

    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        nombre_propietario = request.POST.get('nombre_propietario', '')
        tipo_dni = (request.POST.get('tipo_dni') or '').strip()
        dni = request.POST.get('dni', '')
        username = request.POST.get('username', '').upper()
        email = request.POST.get('email', '')

        if not tipo_dni:
            messages.warning(request, 'Debe escoger un tipo de documento (Venezolano, RIF, Jurídico, etc.).', extra_tags='alert-danger')
        else:
            checkUser = Usuario.objects.filter(email=email)

            # Se revisa si es el mismo usuario
            if checkUser.exists():
                checkActualUser = Usuario.objects.get(id=id)
                checkEmailUser = Usuario.objects.get(email=email)

                if checkActualUser.id == checkEmailUser.id:
                    # Es el mismo usuario
                    propietarios.update(nombre_propietario=nombre_propietario, tipo_dni=tipo_dni, dni=dni)

                    Usuario.objects.filter(pk=id).update(username=username, email=email)

                    messages.success(request, 'El administrador se ha actualizado exitosamente', extra_tags='alert-success')
                    return HttpResponseRedirect(reverse('condominio_app:admin_cuentas'))
                else:
                    messages.warning(request,
                                     'Ha ocurrido un error durante la actualización. El correo electrónico ya esta en uso.',
                                     extra_tags='alert-danger')

            else:
                propietarios.update(nombre_propietario=nombre_propietario,
                                    tipo_dni=tipo_dni, dni=dni)

                Usuario.objects.filter(pk=id).update(username=username, email=email)

                messages.success(request, 'El administrador se ha actualizado exitosamente', extra_tags='alert-success')
                return HttpResponseRedirect(reverse('condominio_app:admin_propietarios'))

    return render(request, 'administrador/update/cuentas_update.html', {'propietarios': propietarios,
                                                                        'usuarios': usuarios, 'conf': conf,
                                                                        'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro})


@login_required
def updateNoticia(request, slug):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    conf = Condominio.objects.filter(id_condominio=user.id_condominio_id)
    noticia = get_object_or_404(Noticia, slug=slug, id_condominio_id=user.id_condominio_id)
    ultima_tasa = Tasas.objects.all().last()
    today = timezone.now()

    tasa_bs = ultima_tasa.tasa_BCV_USD
    tasa_euro = ultima_tasa.tasa_BCV_EUR

    tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                           today.strftime("%A"), tasa_bs, tasa_euro)

    tasa_bs = tasas['tasa_BCV_USD']
    tasa_euro = tasas['tasa_BCV_EUR']

    if request.method == 'POST':
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=noticia)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            noticia = obj
            messages.success(request, 'La noticia o comunicado se ha actualizado exitosamente!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:admin_noticias'))

        else:
            messages.warning(request, 'Ha ocurrido un error durante la actualización. Verifique e intente de nuevo',
                             extra_tags='alert-danger')

    form = UpdateBlogPostForm(
        initial={
            "titulo": noticia.titulo,
            "descripcion": noticia.descripcion,
            "imagen": noticia.imagen,
        }
    )

    return render(request, 'administrador/update/noticias_update.html', {'noticia': form, 'conf': conf,
                                                                         'tasa_bs': tasa_bs, 'tasa_euro': tasa_euro})


# ------------------------------DELETE VIEWS------------------------------
@login_required
def destroyBancos(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    bancos = Bancos.objects.get(id_banco=id)
    movimientos = Movimientos_bancarios.objects.filter(id_banco=id)

    if movimientos.exists():
        if len(movimientos) == 1:
            for mov in movimientos:
                if mov.descripcion_movimiento == "Saldo de Apertura":
                    bancos.delete()
                    messages.success(request, '¡El banco ha sido eliminado de manera satisfactoria!', extra_tags='alert-success')
        else:
            messages.warning(request, '¡El banco no puede ser eliminado debido a que cuenta con movimientos!', extra_tags='alert-danger')
    else:
        messages.success(request, '¡El banco ha sido eliminado de manera satisfactoria!', extra_tags='alert-success')
        bancos.delete()

    return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "bancos"}))

@login_required
def destroyGastos(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    mov = Movimientos_bancarios.objects.select_related("id_banco").get(id_movimiento=id)
    cierre = Cierre_mes.objects.filter(id_condominio_id=user.id_condominio_id).order_by('fecha_cierre').last()
    if cierre and mov.fecha_movimiento:
        cierre_date = cierre.fecha_cierre.date()
        fecha_gasto = mov.fecha_movimiento
        mov_created_at = mov.created_at
        if (
            fecha_gasto < cierre_date
            or (
                fecha_gasto == cierre_date
                and (not mov_created_at or mov_created_at <= cierre.fecha_cierre)
            )
        ):
            messages.warning(request, 'No puedes eliminar un gasto de un mes ya cerrado.', extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:admin_gastos'))

    mov.id_banco.saldo_actual += mov.monto_movimiento
    mov.id_banco.debitos_banco += mov.monto_movimiento
    mov.id_banco.save()
    mov.delete()

    messages.success(request, '¡El gasto ha sido eliminado de manera satisfactoria!', extra_tags='alert-success')
    
    return HttpResponseRedirect(reverse('condominio_app:admin_gastos'))


@login_required
def destroyIngresos(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    mov = Movimientos_bancarios.objects.select_related("id_banco").get(id_movimiento=id)
    banco = mov.id_banco
    monto = mov.monto_movimiento or Decimal('0')

    # Actualizar banco: revertir crédito
    banco.saldo_actual = (banco.saldo_actual or Decimal('0')) - monto
    banco.creditos_banco = (banco.creditos_banco or Decimal('0')) - monto
    banco.save()

    # Actualizar fondos del condominio (saldo_edificio) para mantener coherencia con el banco.
    # "Saldo de Apertura" no se suma al condominio al crear el banco, por tanto no se resta aquí.
    if banco.id_condominio_id and (mov.descripcion_movimiento or '') != 'Saldo de Apertura':
        condominio = Condominio.objects.get(pk=banco.id_condominio_id)
        ultima_tasa = Tasas.objects.all().last()
        tasa_bs = Decimal(str(ultima_tasa.tasa_BCV_USD)) if ultima_tasa and ultima_tasa.tasa_BCV_USD else Decimal('0')
        tasa_euro = Decimal(str(ultima_tasa.tasa_BCV_EUR)) if ultima_tasa and ultima_tasa.tasa_BCV_EUR else Decimal('0')
        if banco.tipo_moneda == 'BS':
            condominio.saldo_edificio = (condominio.saldo_edificio or Decimal('0')) - monto
        elif banco.tipo_moneda == 'USD':
            usd_cambio = tasa_bs * monto
            condominio.saldo_edificio_usd = (condominio.saldo_edificio_usd or Decimal('0')) - usd_cambio
        elif banco.tipo_moneda == 'EUR':
            eur_cambio = tasa_euro * monto
            condominio.saldo_edificio_eur = (condominio.saldo_edificio_eur or Decimal('0')) - eur_cambio
        condominio.save()

    mov.delete()

    messages.success(request, '¡El ingreso ha sido eliminado de manera satisfactoria!', extra_tags='alert-success')
    return HttpResponseRedirect(reverse('condominio_app:admin_ingresos'))


@login_required
def destroyPropietarios(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    propietarios = Propietario.objects.get(id_propietario=id)

    # Desasociar del propietario todo lo que lo referencia para borrado completo en BD
    Domicilio.objects.filter(id_propietario_id=id).update(id_propietario_id=None)
    Ingresos.objects.filter(id_propietario_id=id).update(id_propietario_id=None)

    # Borrar primero el propietario, luego el usuario (evita bloqueos por FK y permite reutilizar DNI)
    propietarios.delete()
    if propietarios.id_usuario_id:
        Usuario.objects.filter(pk=propietarios.id_usuario_id).delete()

    messages.success(request, '¡El registro del propietario y su usuario han sido eliminados de manera satisfactoria!',
                     extra_tags='alert-success')

    return HttpResponseRedirect(reverse('condominio_app:admin_propietarios'))

@login_required
def destroyDeudas(request, id):
    deudas = Deudas.objects.get(id_deuda=id)
    deudas.delete()

    messages.success(request, '¡La deuda ha sido eliminada de manera satisfactoria!',
                     extra_tags='alert-success')

    return HttpResponseRedirect(reverse('condominio_app:admin_deudas'))


@login_required
def destroyCuenta(request, id):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    usuarios = Usuario.objects.get(id=id)

    if usuarios.is_superuser == True:
        messages.warning(request,
                         'Ha ocurrido un error. ¡No puedes eliminar una cuenta con privilegios de súper administrador!',
                         extra_tags='alert-danger')
        return HttpResponseRedirect(reverse('condominio_app:home_admin'))

    else:
        # No es súper administrador el registro que se intenta borrar
        if request.user.id == usuarios.id:
            # El mismo usuario se intenta eliminar
            messages.warning(request, 'Ha ocurrido un error. ¡No puedes eliminar tu propia cuenta desde este modulo!',
                             extra_tags='alert-danger')
            return HttpResponseRedirect(reverse('condominio_app:home_admin'))
        else:
            # No es el mismo usuario; si es propietario, desasociar todo antes para borrado completo (permite reutilizar DNI)
            propietarios = Propietario.objects.get(id_usuario_id=usuarios.id)
            id_prop = propietarios.id_propietario
            Domicilio.objects.filter(id_propietario_id=id_prop).update(id_propietario_id=None)
            Ingresos.objects.filter(id_propietario_id=id_prop).update(id_propietario_id=None)
            propietarios.delete()
            usuarios.delete()

            messages.success(request, '¡El usuario ha sido eliminado de manera satisfactoria!',
                             extra_tags='alert-success')
            return HttpResponseRedirect(reverse('condominio_app:home_admin'))


@login_required
def destroyTorres(request, id):
    torres = Torre.objects.get(id_torre=id)
    if Domicilio.objects.filter(id_torre=id).exists():
        messages.warning(request, '¡La torre no puede ser eliminada debido a que cuenta con apartamentos registrados!',
                         extra_tags='alert-danger')
    else:
        torres.delete()
        messages.success(request, '¡La torre ha sido eliminada de manera satisfactoria!',
                     extra_tags='alert-success')
    return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "torres"}))

@login_required
def destroyDom(request, id):
    dom = Domicilio.objects.get(id_domicilio=id)
    print("\n" + "=" * 60)
    print("⚠️  CONFIRMACIÓN DE ELIMINACIÓN DE DOMICILIO")
    print("=" * 60)
    print(f"📋 Domicilio ID: {dom.id_domicilio}")
    print(f"🏠 Nombre: {dom.nombre_domicilio}")
    if dom.id_propietario_id:
        print(f"⚠️  ADVERTENCIA: Este domicilio tiene un propietario asociado (ID: {dom.id_propietario_id})")
        print("   El propietario será desasociado antes de eliminar el domicilio.")
    print("=" * 60)
    print("❓ ¿Desea eliminar este domicilio?")
    print("   Respuesta: SÍ - Procediendo con la eliminación...")
    print("=" * 60 + "\n")
    
    if dom.id_propietario_id:
        dom.id_propietario_id = None
        dom.save()
        print(f"✅ Propietario desasociado del domicilio {dom.nombre_domicilio}")
    
    dom.delete()
    print(f"✅ Domicilio '{dom.nombre_domicilio}' eliminado exitosamente!")
    print("=" * 60 + "\n")
    
    messages.success(request, '¡El domicilio fue eliminado de manera satisfactoria!',
                     extra_tags='alert-success')
    return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "domicilios"}))
#Editar configuracion/domicilio
@login_required
def updateDom(request, id_domicilio):
    dom = Domicilio.objects.get(id_domicilio=id_domicilio)
    domicilio = Domicilio.objects.get(id_domicilio=id_domicilio)
    alicuota_display = _alicuota_para_display(domicilio)
    return render(request, 'administrador/update/domicilio_update.html', {
        'domicilio': domicilio,
        'alicuota_display': alicuota_display,
    })  
    
                

@login_required
def domicilio_update(request):
    
    prop = Propietario.objects.all()

    id_domicilio = request.POST['txtCodigo']
    nombre_domicilio = request.POST['txtNombreDomicilio']
    tipo_domicilio = request.POST['txtTipoDomicilio']
    piso_domicilio = request.POST['txtPisos']
    zise_domicilio = request.POST['txtZiseDomicilio']
    estacionamientos = request.POST['txtEstacionamientos']
    domicilioUpdate = Domicilio.objects.get(id_domicilio=id_domicilio)
    domicilioUpdate.id_domicilio = id_domicilio
    domicilioUpdate.nombre_domicilio = nombre_domicilio
    domicilioUpdate.tipo_domicilio = tipo_domicilio 
    domicilioUpdate.estacionamientos = estacionamientos
    domicilioUpdate.id_domicilio = id_domicilio
    domicilioUpdate.piso_domicilio = piso_domicilio



    domicilioUpdate.zise_domicilio = zise_domicilio
    domicilioUpdate.save()

    messages.success(request, '¡El domicilio fue actualizado de manera satisfactoria!',extra_tags='alert-success')
    return HttpResponseRedirect(reverse('condominio_app:admin_configuracion', kwargs={'type': "domicilios"}))


@login_required
def destroyNoticia(request, slug):
    user = request.user
    # Si el usuario no es un administrador entonces se le redirigirá a la página de propietarios
    # Solo redirigir a propietarios si tiene rol 2-5 y no está asignado como admin de un condominio
    if user.id_rol and str(user.id_rol.rol) in ('2', '3', '4', '5') and user.id_condominio_id is None:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    noticia = get_object_or_404(Noticia, slug=slug, id_condominio_id=user.id_condominio_id)
    noticia.delete()

    messages.success(request, '¡La noticia ha sido eliminado de manera satisfactoria!', extra_tags='alert-success')
    return HttpResponseRedirect(reverse('condominio_app:admin_noticias'))

# ------------------------------DESCARGAR------------------------------
def downloadReferencia(request):

    gasto = Gastos.objects.select_related("id_movimiento").get(id_gasto=request.POST['id_gasto'])

    fecha_hora = str(gasto.id_movimiento.created_at.strftime('%d/%m/%Y')) + " " + str(gasto.id_movimiento.created_at.strftime('%H:%M:%S'))
    name = str(gasto.id_movimiento.concepto_movimiento) + "-" + str(fecha_hora) + ".jpg"

    ruta = os.path.join(settings.MEDIA_ROOT, request.POST['ruta_imagen'])
    imagen = open(ruta, 'rb')
    response = FileResponse(imagen)
    response['Content-Disposition'] = 'attachment; filename=' + str(name) + ''
    return response

def downloadReferenciaingreso(request):

    ingreso = Ingresos.objects.select_related("id_movimiento").get(id_ingreso=request.POST['id_ingreso'])

    fecha_hora = str(ingreso.id_movimiento.created_at.strftime('%d/%m/%Y')) + " " + str(ingreso.id_movimiento.created_at.strftime('%H:%M:%S'))
    name = str(ingreso.id_movimiento.concepto_movimiento) + "-" + str(fecha_hora) + ".jpg"

    ruta = os.path.join(settings.MEDIA_ROOT, request.POST['ruta_imagen'])
    imagen = open(ruta, 'rb')
    response = FileResponse(imagen)
    response['Content-Disposition'] = 'attachment; filename=' + str(name) + ''
    return response

# ------------------------------VIEWS ESPECIALES------------------------------
def enviar_email(request, id):
    user = request.user
    if user.id_rol_id == 2 or user.id_rol_id == 3 or user.id_rol_id == 4 or user.id_rol_id == 5:
        return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

    propietarios = Propietario.objects.get(id_propietario=id)
    usuario = Usuario.objects.get(username=propietarios.apto)

    dataEmail = {
        'propietario': propietarios.nombre_propietario,
        'apto': propietarios.apto,
        'password': usuario.password
    }

    html_content = render_to_string('mails/mail.html', dataEmail)

    email = EmailMultiAlternatives('Esparta Suites: Información de Cuenta', html_content)
    email.attach_alternative(html_content, "text/html")
    email.to = [usuario.email]
    res = email.send()
    if (res == 1):
        print("Correo enviado satisfactoriamente")
    messages.success(request, '¡El email ha sido enviado correctamente!', extra_tags='alert-success')
    return HttpResponseRedirect(reverse('condominio_app:home_admin'))


def enviar_consulta(request):
    if request.method == 'POST':
        send_mail(
            request.POST['subject'],
            request.POST['body'],
            request.POST['email'],
            ['gustavordgz15@gmail.com'],
            fail_silently=False,
        )


def redireccion_de_usuario(request):
    """Redirige: HEADADMIN → home_superuser; admin/propietario → inicio_condominio (inicio de su condominio)."""
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('condominio_app:home'))
    tipo = _tipo_panel_usuario(user)
    if tipo == 'superuser':
        return HttpResponseRedirect(reverse('condominio_app:home_superuser'))
    if tipo in ('admin', 'propietario'):
        return HttpResponseRedirect(reverse('condominio_app:inicio_condominio'))
    return HttpResponseRedirect(reverse('condominio_app:home_propietarios'))

@require_http_methods(['GET'])
def obtener_pisos(request):

    if request.GET.get('id_prop'):
        domicilio = Domicilio.objects.filter(id_propietario_id=request.GET.get('id_prop'))
        idTorre = request.GET.get('torre')
        torre = Torre.objects.get(id_torre=idTorre)

        pisos = [('0', 'Seleccione un piso...')]
        for i in range(int(torre.pisos)):
            pisos.append(((i + 1), (i + 1)))

        piso_seleccionado = []
        for dom in domicilio:
            piso_seleccionado.append(dom.piso_domicilio)

        data = {
            'pisos': pisos,
            'piso_seleccionado': piso_seleccionado
        }
        return JsonResponse(data)

    else:
        idTorre = request.GET.get('torre')
        torre = Torre.objects.get(id_torre=idTorre)

        pisos = [('', 'Seleccione un piso...')]
        for i in range(int(torre.pisos)):
            pisos.append(((i+1), (i+1)))

        data = {
            'pisos': pisos
        }
        return JsonResponse(data)

@require_http_methods(['GET'])
def obtener_inmuebles_propietario(request):
    if request.GET.get('id_propietario'):
        domicilios = Domicilio.objects.filter(id_propietario_id=request.GET.get('id_propietario'))
        inmuebles = []
        for domicilio in domicilios:
            inmuebles.append({
                'id': domicilio.id_domicilio,
                'nombre': domicilio.nombre_domicilio
            })

        data = {
            'inmuebles': inmuebles
        }
        return JsonResponse(data)

    return JsonResponse({'inmuebles': []})

@require_http_methods(['GET'])
def obtener_bancos(request):

    if request.GET.get('tipo_moneda') == "BS":

        bancos = [('100% BANCO','100% BANCO'),
                  ('BANCAMIGA','BANCAMIGA'),
                  ('BANCO ACTIVO','BANCO ACTIVO'),
                  ('BANCO AGRICOLA DE VENEZUELA','BANCO AGRICOLA DE VENEZUELA'),
                  ('BANCO BICENTENARIO','BANCO BICENTENARIO'),
                  ('BANCO CARONÍ','BANCO CARONÍ'),
                  ('BANCO DE COMERCIO EXTERIOR','BANCO DE COMERCIO EXTERIOR'),
                  ('BANCO DE LA FUERZA ARMADA NACIONAL BOLIVARIANA','BANCO DE LA FUERZA ARMADA NACIONAL BOLIVARIANA'),
                  ('BANCO DE VENEZUELA','BANCO DE VENEZUELA'),
                  ('BANCO DEL CARIBE', 'BANCO DEL CARIBE'),
                  ('BANCO DEL TESORO','BANCO DEL TESORO'),
                  ('BANCO EXTERIOR','BANCO EXTERIOR'),
                  ('BANCO INTERNACIONAL DE DESARROLLO','BANCO INTERNACIONAL DE DESARROLLO'),
                  ('BANCO NACIONAL DE CRÉDITO','BANCO NACIONAL DE CRÉDITO'),
                  ('BANCO PLAZA','BANCO PLAZA'),
                  ('BANCO PROVINCIAL','BANCO PROVINCIAL'),
                  ('BANCO SOFITASA','BANCO SOFITASA'),
                  ('BANCRECER','BANCRECER'),
                  ('BANESCO','BANESCO'),
                  ('BANPLUS','BANPLUS'),
                  ('BFC BANCO FONDO COMUN','BFC BANCO FONDO COMUN'),
                  ('DEL SUR','DEL SUR'),
                  ('MERCANTIL','MERCANTIL'),
                  ('VENEZOLANO DE CRÉDITO','VENEZOLANO DE CRÉDITO')]

        print(len(bancos))

        data = {
            'bancos': bancos,
            'cantidad_bancos': len(bancos)
        }

        return JsonResponse(data)

    elif request.GET.get('tipo_moneda') == "USD":
        bancos = [('BANK OF AMERICA', 'BANK OF AMERICA'),
                  ('CITIBANK', 'CITIBANK'),
                  ('PAYPAL', 'PAYPAL'),
                  ('ZELLE', 'ZELLE'),
                  ('CAJA CHICA - FONDO EFECTIVO $', 'CAJA CHICA - FONDO EFECTIVO $')]

        print(len(bancos))

        data = {
            'bancos': bancos,
            'cantidad_bancos': len(bancos)
        }

        return JsonResponse(data)

    elif request.GET.get('tipo_moneda') == "EUR":
        bancos = [('BBVA', 'BBVA'),
                  ('BANCO SANTANDER', 'BANCO SANTANDER')]

        print(len(bancos))

        data = {
            'bancos': bancos,
            'cantidad_bancos': len(bancos)
        }

        return JsonResponse(data)

def _alicuota_para_display(domicilio):
    """Devuelve la alícuota en formato decimal (0.16 para 16%): guardada o calculada por m²."""
    if domicilio.alicuota_domicilio is not None:
        a = float(domicilio.alicuota_domicilio)
        # Si viene como % (16), convertir a decimal (0.16); si ya es decimal (0.16), mantener
        return round((a / 100) if a > 1 else a, 4)
    if not domicilio.id_condominio_id:
        return None
    try:
        condominio = Condominio.objects.get(id_condominio=domicilio.id_condominio_id)
    except Condominio.DoesNotExist:
        return None
    total_m2 = getattr(condominio, 'superficie_total_m2', None)
    if total_m2 is None or total_m2 <= 0:
        total_m2 = Decimal('0')
        for d in Domicilio.objects.filter(id_condominio_id=domicilio.id_condominio_id):
            try:
                val = d.size_domicilio
                if val is not None and str(val).strip():
                    total_m2 += Decimal(str(val).replace(',', '.'))
            except (TypeError, ValueError):
                pass
    try:
        m2_dom = Decimal(str(domicilio.size_domicilio).replace(',', '.')) if domicilio.size_domicilio else Decimal('0')
    except (TypeError, ValueError):
        m2_dom = Decimal('0')
    if total_m2 and total_m2 > 0 and m2_dom > 0:
        return round(float(m2_dom / total_m2), 4)
    return None


@require_http_methods(['GET'])
def obtener_deudas(request):
    if request.GET.get('aptoDeuda'):
        domicilio = Domicilio.objects.get(id_domicilio=request.GET.get('aptoDeuda'))
        alicuota_display = _alicuota_para_display(domicilio)
        if domicilio.id_torre_id:
            torre = Torre.objects.get(id_torre=domicilio.id_torre_id)

            if domicilio.piso_domicilio:
                piso = domicilio.piso_domicilio
            else:
                piso = "-"

            deudas = Deudas.objects.filter(id_domicilio_id=request.GET.get('aptoDeuda'), is_active=True).order_by('categoria_deuda')

            data = {
                'domicilio': {
                    'id': domicilio.id_domicilio,
                    'nombre': domicilio.nombre_domicilio,
                    'piso': piso,
                    'torre': "-",
                    'estacionamientos': domicilio.estacionamientos,
                    'size': domicilio.size_domicilio,
                    'alicuota': alicuota_display if alicuota_display is not None else domicilio.alicuota_domicilio,
                    'saldo_bs': domicilio.saldo,
                    'saldo_usd': domicilio.saldo_usd,
                    'saldo_eur': domicilio.saldo_eur,
                },
                'deudas': list(deudas.values()),
                'cantidad_deudas': len(deudas)
            }

        else:

            if domicilio.piso_domicilio:
                piso = domicilio.piso_domicilio
            else:
                piso = "-"

            
            deudas = Deudas.objects.filter(id_domicilio_id=request.GET.get('aptoDeuda'), is_active=True).order_by('categoria_deuda')

            data = {
                'domicilio': {
                    'id': domicilio.id_domicilio,
                    'nombre': domicilio.nombre_domicilio,
                    'piso': piso,
                    'torre': "-",
                    'estacionamientos': domicilio.estacionamientos,
                    'size': domicilio.size_domicilio,
                    'alicuota': alicuota_display if alicuota_display is not None else domicilio.alicuota_domicilio,
                    'saldo_bs': domicilio.saldo,
                    'saldo_usd': domicilio.saldo_usd,
                    'saldo_eur': domicilio.saldo_eur,
                },
                'deudas': list(deudas.values()),
                'cantidad_deudas': len(deudas)
            }

        return JsonResponse(data)

@require_http_methods(['GET'])
def eliminar_publicacion(request):
    if request.GET.get('publicacion'):
        post = Alquiler.objects.get(id_alquiler=request.GET.get('publicacion'))
        post.delete()

        data = {
            'success': True
        }

        return JsonResponse(data)

    else:
        data = {
            'success': False
        }

        return JsonResponse(data)

@require_http_methods(['GET'])
def cambiar_monto(request):
    if request.GET.get('moneda_seleccionada'):

        bancos = list(Bancos.objects.filter(
            id_condominio_id=request.user.id_condominio_id,
            tipo_moneda=request.GET.get('moneda_seleccionada')
        ).values())

        ultima_tasa = Tasas.objects.last()
        today = timezone.now()

        tasa_bs = ultima_tasa.tasa_BCV_USD
        tasa_euro = ultima_tasa.tasa_BCV_EUR

        tasas = comprobar_tasa(request, today.strftime("%d/%m/%Y"), ultima_tasa.updated_at.strftime("%d/%m/%Y"),
                               today.strftime("%A"), tasa_bs, tasa_euro)

        tasa_bs = Decimal(tasas['tasa_BCV_USD'])
        tasa_euro = Decimal(tasas['tasa_BCV_EUR'])

        data_condo = json.loads(request.GET.get('deuda_condo'))
        data_cuota = json.loads(request.GET.get('deuda_cuota'))

        monto_condo = []
        monto_cuota = []

        print(data_condo)
        print(data_cuota)

        def convert_monto(monto, moneda_origen, moneda_destino):
            monto = Decimal(monto)
            if moneda_origen == moneda_destino:
                return monto
            if moneda_destino == "BS":
                if moneda_origen == "USD":
                    return monto * tasa_bs
                if moneda_origen == "EUR":
                    return monto * tasa_euro
            if moneda_destino == "USD":
                if moneda_origen == "BS":
                    return monto / tasa_bs
                if moneda_origen == "EUR":
                    return (monto * tasa_euro) / tasa_bs
            if moneda_destino == "EUR":
                if moneda_origen == "BS":
                    return monto / tasa_euro
                if moneda_origen == "USD":
                    return (monto * tasa_bs) / tasa_euro
            return monto

        if all(not data for data in data_condo):
            pass
        else:
            for monto, moneda in zip(data_condo[0], data_condo[1]):
                resultado = convert_monto(monto, moneda, request.GET.get('moneda_seleccionada'))
                monto_condo.append(round(resultado, 2))

        if all(not data for data in data_cuota):
            pass
        else:
            for monto, moneda in zip(data_cuota[0], data_cuota[1]):
                resultado = convert_monto(monto, moneda, request.GET.get('moneda_seleccionada'))
                monto_cuota.append(round(resultado, 2))

        data = {
            'monto_condo': monto_condo,
            'monto_cuota': monto_cuota,
            'bancos': bancos
        }

        return JsonResponse(data)


@require_http_methods(['GET'])
def obtener_domicilio(request):

    if request.GET.get('domicilio'):
        domicilio = Domicilio.objects.get(id_domicilio=request.GET.get('domicilio'))

        if domicilio.id_torre_id:
            torre = Torre.objects.get(id_torre=domicilio.id_torre_id)

            if domicilio.piso_domicilio:
                piso = domicilio.piso_domicilio
            else:
                piso = "-"

            alic = _alicuota_para_display(domicilio)
            data = {
                'nombre_domicilio': domicilio.nombre_domicilio,
                'piso_domicilio': piso,
                'tipo_domicilio': domicilio.tipo_domicilio,
                'alicuota_domicilio': round(alic, 4) if alic is not None else '',
                'size_domicilio': domicilio.size_domicilio,
                'estacionamientos': domicilio.estacionamientos,
                'nombre_torre': torre.nombre_torre
            }

        else:

            if domicilio.piso_domicilio:
                piso = domicilio.piso_domicilio
            else:
                piso = "-"

            alic = _alicuota_para_display(domicilio)
            data = {
                'nombre_domicilio': domicilio.nombre_domicilio,
                'piso_domicilio': piso,
                'tipo_domicilio': domicilio.tipo_domicilio,
                'alicuota_domicilio': round(alic, 4) if alic is not None else '',
                'size_domicilio': domicilio.size_domicilio,
                'estacionamientos': domicilio.estacionamientos,
                'nombre_torre': "-"
            }

        return JsonResponse(data)

    else:
        idTorre = request.GET.get('torre')
        torre = Torre.objects.get(id_torre=idTorre)

        pisos = [('', 'Seleccione un piso...')]
        for i in range(int(torre.pisos)):
            pisos.append(((i+1), (i+1)))

        data = {
            'pisos': pisos
        }
        return JsonResponse(data)


def get_publicacion_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Noticia.objects.filter(
            Q(titulo__icontains=q) |
            Q(descripcion__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))


def link_callback(uri, rel):
    """
  Convert HTML URIs to absolute system paths so xhtml2pdf can access those
  resources
  """
    def is_subpath(path, parent):
        try:
            return os.path.commonpath([path, parent]) == parent
        except ValueError:
            return False

    # xhtml2pdf may pass absolute Windows paths (e.g. C:\static\...) or file:// URIs
    uri_path = uri
    if uri.startswith("file://"):
        try:
            from urllib.parse import urlparse, unquote
            uri_path = unquote(urlparse(uri).path)
            if len(uri_path) > 3 and uri_path[0] == "/" and uri_path[2] == ":":
                uri_path = uri_path[1:]
        except Exception:
            uri_path = uri.replace("file://", "")

    drive, _ = os.path.splitdrive(uri_path)
    if os.path.isabs(uri_path) or drive:
        abs_uri = os.path.realpath(uri_path)
        static_root = os.path.realpath(getattr(settings, "STATIC_ROOT", "") or "")
        media_root = os.path.realpath(getattr(settings, "MEDIA_ROOT", "") or "")
        base_static = os.path.realpath(os.path.join(settings.BASE_DIR, "static"))
        static_dirs = [
            os.path.realpath(p) for p in getattr(settings, "STATICFILES_DIRS", []) or []
        ]

        # Remap C:\static\... to the project's static directory
        if abs_uri.lower().startswith(os.path.normpath("C:\\static").lower()):
            rel_path = os.path.relpath(abs_uri, os.path.normpath("C:\\static"))
            abs_uri = os.path.realpath(os.path.join(base_static, rel_path))

        allowed_roots = [p for p in [static_root, media_root, base_static] if p] + static_dirs
        if any(is_subpath(abs_uri, root) for root in allowed_roots) and os.path.isfile(abs_uri):
            return abs_uri
        if os.path.isfile(abs_uri):
            return abs_uri
        return abs_uri

    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

# def limpiar_db(request):
#     Domicilio.objects.all().delete()
#     Propietario.objects.all().delete()
#     Ingresos.objects.all().delete()
#     Gastos.objects.all().delete()
#     Bancos.objects.all().delete()
#     Cierre_mes.objects.all().delete()
#     Noticia.objects.all().delete()
#     Torre.objects.all().delete()
#     Fondos.objects.all().delete()

#     return render(request, 'administrador/home.html')


# def eliminar_elemento(request):
#     Usuario.objects.get(username='4526274').delete()

#     return render(request, 'administrador/home.html')

def agregar_elemento(request):
    # user = Usuario.objects.get(id=1)
    # user.id_rol_id = 0
    # user.id_condominio_id = 1
    # user.save()

    rol = Rol()

    rol.rol = 'Administrador'
    rol.save()
    rol.rol = 'Presidente'
    rol.save()
    rol.rol = 'Secretario/a'
    rol.save()
    rol.rol = 'Junta'
    rol.save()
    rol.rol = 'Propietario'
    rol.save()
    rol.rol = 'Portero'
    rol.save()

    return render(request, 'administrador/home.html')