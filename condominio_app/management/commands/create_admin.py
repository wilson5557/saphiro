"""
Comando para crear un usuario administrador inicial
Uso: python manage.py create_admin
"""
from django.core.management.base import BaseCommand
from condominio_app.models import Usuario, Rol, Condominio
from django.db import transaction


class Command(BaseCommand):
    help = 'Crea un usuario administrador inicial con rol y condominio'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Nombre de usuario',
            default='admin'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Correo electrónico',
            default='admin@condominio.com'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Contraseña',
            default='admin123'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Verificar si ya existe el usuario (eliminar si existe para recrearlo)
        username_upper = username.upper()
        if Usuario.objects.filter(username=username_upper).exists():
            self.stdout.write(
                self.style.WARNING(f'⚠️  El usuario "{username_upper}" ya existe. Eliminándolo para recrearlo...')
            )
            Usuario.objects.filter(username=username_upper).delete()

        # Crear o obtener rol de administrador
        # Primero intentar obtener un rol existente con id_rol=0 o 1
        rol_admin = None
        try:
            rol_admin = Rol.objects.filter(id_rol__in=[0, 1]).first()
            if not rol_admin:
                # Crear nuevo rol ADMIN
                rol_admin = Rol.objects.create(rol='ADMIN')
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Rol ADMIN creado (id_rol={rol_admin.id_rol})')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Usando rol existente: {rol_admin.rol} (id_rol={rol_admin.id_rol})')
                )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️  Error al obtener/crear rol: {e}. Continuando sin rol...')
            )

        # Crear o obtener condominio por defecto
        condominio = None
        try:
            condominio = Condominio.objects.first()
            if not condominio:
                # Crear condominio por defecto
                condominio = Condominio.objects.create(
                    nombre_condominio='Condominio Principal',
                    rif_condominio='J-00000000-0',
                    direccion_condominio='Dirección por defecto'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Condominio por defecto creado (id={condominio.id_condominio})')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Usando condominio existente: {condominio.nombre_condominio} (id={condominio.id_condominio})')
                )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️  Error al obtener/crear condominio: {e}. Continuando sin condominio...')
            )

        # Crear el superusuario
        try:
            # Asegurar que el username esté en mayúsculas para consistencia
            if 'username_upper' not in locals():
                username_upper = username.upper()
            usuario = Usuario.objects.create_user(
                username=username_upper,
                email=email,
                password=password
            )
            usuario.is_superuser = True
            usuario.is_admin = True
            usuario.is_staff = True
            
            if rol_admin:
                usuario.id_rol_id = rol_admin.id_rol
            if condominio:
                usuario.id_condominio_id = condominio.id_condominio
                
            usuario.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Usuario administrador creado exitosamente!\n'
                    f'   Username: {username_upper}\n'
                    f'   Email: {email}\n'
                    f'   Password: {password}\n'
                    f'   Rol ID: {usuario.id_rol_id if rol_admin else "No asignado"}\n'
                    f'   Condominio ID: {usuario.id_condominio_id if condominio else "No asignado"}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠️  IMPORTANTE: Cambia la contraseña después del primer inicio de sesión!'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error al crear usuario: {str(e)}')
            )
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
