"""
Asigna un condominio a un usuario administrador existente (para que vaya al panel admin y no al de superusuario).

Uso:
  python manage.py asignar_condominio_admin --username ADMIN
  python manage.py asignar_condominio_admin --username ADMIN --condominio-id 1
"""
from django.core.management.base import BaseCommand
from condominio_app.models import Usuario, Condominio


class Command(BaseCommand):
    help = 'Asigna id_condominio a un usuario admin para que entre al panel de administración (no al de superusuario)'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Username del administrador (ej. ADMIN)')
        parser.add_argument('--condominio-id', type=int, default=None, help='ID del condominio (si no se pasa, se usa el primero)')

    def handle(self, *args, **options):
        username = (options['username'] or '').strip().upper()
        if not username:
            self.stdout.write(self.style.ERROR('Indique --username'))
            return
        try:
            usuario = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            self.stdout.write(self.style.ERROR('No existe usuario con username "{}"'.format(username)))
            return
        condominio_id = options.get('condominio_id')
        if condominio_id is None:
            c = Condominio.objects.first()
            if not c:
                self.stdout.write(self.style.ERROR('No hay condominios. Cree uno desde el panel superusuario.'))
                return
            condominio_id = c.id_condominio
        else:
            try:
                Condominio.objects.get(pk=condominio_id)
            except Condominio.DoesNotExist:
                self.stdout.write(self.style.ERROR('No existe condominio con id {}'.format(condominio_id)))
                return
        usuario.id_condominio_id = condominio_id
        usuario.save(update_fields=['id_condominio_id'])
        self.stdout.write(
            self.style.SUCCESS(
                'Usuario "{}" asignado al condominio id={}. Al iniciar sesión irá al panel de administración.'.format(username, condominio_id)
            )
        )
