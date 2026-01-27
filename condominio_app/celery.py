from __future__ import absolute_import
from datetime import timedelta
from django.conf import settings  # noqa
from celery import Celery
from celery.schedules import crontab
import os


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'condominio.settings')
app = Celery('condominio', broker='redis://localhost:6379/0', backend='django-db')

# db+postgresql://user:password@localhost/mydatabase
# db+postgresql://postgres:151925@localhost/condo_db


app.config_from_object('django.conf:settings', namespace='CELERY')

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'cuota_mensual': {
        'task': 'condominio_app.tasks.cuota_base',
        'schedule': crontab(day_of_month='1', hour='0', minute='0'),
    },
    'cobrar_saldo': {
        'task': 'condominio_app.tasks.cobro_saldo',
        'schedule': crontab(hour='11', minute='59'),
    },
    'cobrar_saldo2': {
        'task': 'condominio_app.tasks.cobro_saldo',
        'schedule': crontab(hour='23', minute='59'),
    },
    'fecha_cobro_con_d': {
        'task': 'condominio_app.tasks.restar_saldo',
        'schedule': crontab(day_of_month='5', hour='12', minute='0'),
    },
    'actualizacion1_tasa': {
        'task': 'condominio_app.tasks.comprobar_tasa',
        'schedule': crontab(hour='9', minute='0'),
    },
    'actualizacion2_tasa': {
        'task': 'condominio_app.tasks.comprobar_tasa',
        'schedule': crontab(hour='15', minute='0'),
    },
}

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))