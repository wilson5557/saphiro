"""
Comando para probar el envío de correo (reportes, etc.).
Uso: python manage.py send_test_email correo@ejemplo.com
Si no llegan los reportes por correo, ejecuta esto para ver el error real.
"""
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import sys


class Command(BaseCommand):
    help = 'Envía un correo de prueba para verificar SMTP (Gmail, etc.). Si falla, muestra el error.'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Correo de destino (ej. tutora@ejemplo.com)',
        )

    def handle(self, *args, **options):
        dest = options['email']
        from_email = getattr(settings, 'EMAIL_HOST_USER', None) or getattr(settings, 'DEFAULT_FROM_EMAIL', '')
        self.stdout.write('Enviando correo de prueba a: {}'.format(dest))
        self.stdout.write('Desde (EMAIL_HOST_USER): {}'.format(from_email))
        self.stdout.write('Backend: {}'.format(getattr(settings, 'EMAIL_BACKEND', '?')))
        if 'console' in str(getattr(settings, 'EMAIL_BACKEND', '')).lower():
            self.stderr.write(self.style.ERROR(
                'ERROR: El backend de correo está en CONSOLA. Los reportes no se envían por correo real. '
                'En settings.py debe estar: EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"'
            ))
            sys.exit(1)
        try:
            msg = EmailMultiAlternatives(
                'Prueba de correo - Saphiro Condominio',
                'Si recibes este mensaje, el envío de reportes por correo está configurado correctamente.',
                from_email,
                [dest],
            )
            msg.send(fail_silently=False)
            self.stdout.write(self.style.SUCCESS('Correo enviado correctamente. Revisa la bandeja de entrada (y spam) de {}.'.format(dest)))
            self.stdout.write('')
            self.stdout.write('Si los reportes siguen sin llegar, revisa:')
            self.stdout.write('  1. Que el correo del propietario esté bien guardado en la ficha del propietario.')
            self.stdout.write('  2. Carpeta de spam / correo no deseado.')
            self.stdout.write('  3. Gmail: usar contraseña de aplicación (cuenta Google → Seguridad → Contraseñas de aplicación).')
        except Exception as e:
            self.stderr.write(self.style.ERROR('Error al enviar: {}'.format(e)))
            self.stdout.write('')
            self.stdout.write('Posibles soluciones:')
            self.stdout.write('  - Gmail: crear una "Contraseña de aplicación" y ponerla en EMAIL_HOST_PASSWORD (o variable de entorno EMAIL_HOST_PASSWORD).')
            self.stdout.write('  - En la PC donde corre la app, definir: set EMAIL_HOST_USER=tu_correo@gmail.com  y  set EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion')
            sys.exit(1)
