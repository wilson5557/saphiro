import time
from datetime import datetime, time, date
import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.contrib import messages
from django.utils import timezone
from requests import request

from .models import Cuota_mensual, Condominio, Cuotas_extras, Ingresos, Tasas, Propietario, Gastos, Deudas_propietarios, \
    Recargos_y_Descuentos

def cobro(propietario, deuda_prop, moroso):
    if propietario.saldo > 0:
        if moroso == 0:
            deuda_restante = propietario.saldo - deuda_prop.monto_deuda
            if deuda_restante < 0:
                propietario.saldo = 0
                deuda_prop.is_active = False
                deuda_prop.monto_deuda = abs(deuda_restante)
                deuda_prop.save()
                print('¡La deuda no ha sido cancelada en su totalidad aún!')
            else:
                propietario.saldo = deuda_restante
                deuda_prop.is_active = False
                propietario.save()
                deuda_prop.save()
                print('¡La deuda fue pagado con exito!')
        else:
            deuda_restante = propietario.saldo - moroso
            if deuda_restante < 0:
                propietario.saldo = 0
                deuda_prop.monto_deuda = deuda_restante
                deuda_prop.save()
                print('¡La deuda de no ha sido cancelada en su totalidad aún!')
            else:
                propietario.saldo = deuda_restante
                deuda_prop.is_active = True
                propietario.save()
                deuda_prop.save()
                print('¡La deuda fue pagado con exito!')


@shared_task
def cobro_saldo():
    propietarios = Propietario.objects.all()
    deudas = Deudas_propietarios.objects.all()
    morosidad = Recargos_y_Descuentos.objects.all().last()

    for propietario in propietarios:
        for deuda in deudas:
            if propietario.id_propietario == deuda.id_propietario_id and deuda.is_active:
                if deuda.is_moroso:
                    moroso = deuda.monto_deuda * (morosidad.recargo_moratorio / 100)
                    cobro(propietario, deuda, moroso)
                else:
                    moroso = 0
                    cobro(propietario, deuda, moroso)
            else:
                print("wtf no")


@shared_task
def restar_saldo():
    propietarios = Propietario.objects.all()
    cuotas_extras = Cuotas_extras.objects.all().select_related("id_gasto")
    cuota_m = Cuota_mensual.objects.all().last()
    today = timezone.now()

    for propietario in propietarios:
        cuota_extras_prop = Cuotas_extras.objects.filter(id_propietario_id=propietario.id_propietario)

        cuota_extra_all = 0
        cuota_extra_solo = 0
        cuota_descripcion = ""

        for cuotas_extra in cuotas_extras:
            if cuotas_extra.is_all and cuotas_extra.is_active:
                cuota_extra_all = cuota_extra_all + cuotas_extra.monto_cuota
            elif cuotas_extra.id_propietario_id == propietario.id_propietario and cuotas_extra.is_active:
                cuota_extra_solo = cuota_extra_solo + cuotas_extra.monto_cuota
                cuota_descripcion = cuotas_extra.id_gasto.descripcion_gasto

        total_condominio = cuota_m.monto_cuota + cuota_extra_all

        propietario.saldo -= total_condominio

        if propietario.saldo < 0:
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
                     "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

            descripcion = 'Condominio del mes de ' + meses[(today.month - 1)]
            Deudas_propietarios.objects.get_or_create(fecha_deuda=today.date(),
                                                      descripcion=descripcion,
                                                      tipo_deuda='Condominio',
                                                      monto_deuda=abs(propietario.saldo),
                                                      is_active=True, is_moroso=False,
                                                      id_propietario=propietario,
                                                      created_at=timezone.now(), updated_at=timezone.now())
            propietario.estado_deuda = True
        else:
            propietario.estado_deuda = False

        if cuota_extra_solo != 0:

            propietario.saldo -= cuota_extra_solo

            if propietario.saldo < 0:
                Deudas_propietarios.objects.get_or_create(fecha_deuda=today.date(),
                                                          descripcion=cuota_descripcion,
                                                          tipo_deuda='Cuota extra',
                                                          monto_deuda=abs(propietario.saldo),
                                                          is_active=True, is_moroso=False,
                                                          id_propietario=propietario,
                                                          created_at=timezone.now(), updated_at=timezone.now())
                cuota_extras_prop.is_active = True
                propietario.estado_deuda = True
            else:
                cuota_extras_prop.is_active = False
                propietario.estado_deuda = False

        # propietario.save()

    return "¡Saldo de los propietarios para las deudas del mes restado con exito!"


@shared_task
def cuota_base():
    condominio = Condominio.objects.filter(id_condominio=1).values()
    gastos = Gastos.objects.all().values()
    ingresos = Ingresos.objects.all().values()
    pago_mensual = Cuota_mensual.objects.all().last()

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
             "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    saldo_condo = 0
    total_gastos = 0
    total_ingresos = 0

    for condo in condominio:
        saldo_condo = condo['saldo_edificio']

    for gasto in gastos:
        if gasto['tipo_gasto'] == 'COMÚN':
            total_gastos = total_gastos + gasto['monto_gasto']

    for ingreso in ingresos:
        total_ingresos = total_ingresos + ingreso['monto_ingreso']

    resultado = total_gastos + saldo_condo - total_ingresos

    if Cuota_mensual.objects.all().count() != 0:
        if timezone.now().month != pago_mensual.fecha_publicacion.month:
            Cuota_mensual.objects.get_or_create(fecha_publicacion=timezone.now(),
                                                descripcion=meses[(timezone.now().month - 1)],
                                                monto_cuota=resultado, id_condominio=condominio[0]['id_condominio'])
        else:
            return "La cuota base ya fue fijada."
    else:
        Cuota_mensual.objects.get_or_create(fecha_publicacion=timezone.now(),
                                            descripcion=meses[(timezone.now().month - 1)],
                                            monto_cuota=resultado, id_condominio=condominio[0]['id_condominio'])

    return "¡Cuota base definida con exito!"


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
        print(texto_fecha)
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


@shared_task
def comprobar_tasa():
    ultima_tasa = Tasas.objects.all().last()
    hoy = timezone.now()

    fecha_actual = ultima_tasa.updated_at.strftime("%d/%m/%Y")
    dia_semana = hoy.strftime("%A")
    tasa_bolivares = ultima_tasa.tasa_BCV_USD
    tasa_euros = ultima_tasa.tasa_BCV_EUR
    today = hoy.strftime("%d/%m/%Y")

    if today != fecha_actual:
        if dia_semana == 'Monday' or 'Tuesday' or 'Wednesday' or 'Thursday' or 'Friday':
            tasas = actualizar_tasa()
            if tasas['tasa_BCV_USD'] != 0:
                tasa_bolivares = tasas['tasa_BCV_USD']
                tasa_euros = tasas['tasa_BCV_EUR']
                created = Tasas.objects.get_or_create(tasa_BCV_USD=tasa_bolivares,
                                                      tasa_BCV_EUR=tasa_euros,
                                                      created_at=datetime.now(),
                                                      updated_at=datetime.now())
                return 'La tasa fue actualizada correctamente.'
            else:
                messages.warning(request,
                                 '¡Debe establecer la tasa de cambio del día debido a que no se pudo conectar al BCV {}!'.format(
                                     today, extra_tags='alert-danger'))
                return 'La tasa no pudo ser cambiada.'
        elif dia_semana == 'Saturday' or 'Sunday':
            return 'Los fines de semana no cambia la tasa.'
    else:
        return 'El dia no ha cambiado, con lo cual la tasa se mantiene.'
