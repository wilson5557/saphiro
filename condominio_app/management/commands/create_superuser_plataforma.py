"""
Comando para crear el superusuario de la plataforma (gestión de condominios).
Este usuario no pertenece a ningún condominio y accede a la vista de SUPERUSUARIO.

Uso: python manage.py create_superuser_plataforma
     python manage.py create_superuser_plataforma --username super --email super@plataforma.com --password secret
"""
from django.core.management.base import BaseCommand
from condominio_app.models import Usuario, Rol
from django.db import transaction


class Command(BaseCommand):
    help = 'Crea un superusuario de plataforma (sin condominio) para gestionar y crear condominios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Nombre de usuario del superusuario de plataforma',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Correo electrónico del superusuario',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Contraseña del superusuario',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')

        if not username:
            username = input('Username (superusuario plataforma): ').strip()
        if not username:
            self.stdout.write(self.style.ERROR('Se requiere username.'))
            return

        if not email:
            email = input('Email: ').strip()
        if not email:
            self.stdout.write(self.style.ERROR('Se requiere email.'))
            return

        if not password:
            from getpass import getpass
            password = getpass('Password: ')
            password2 = getpass('Password (again): ')
            if password != password2:
                self.stdout.write(self.style.ERROR('Las contraseñas no coinciden.'))
                return
            if not password:
                self.stdout.write(self.style.ERROR('Se requiere contraseña.'))
                return

        username_upper = username.upper()
        if Usuario.objects.filter(username=username_upper).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario "{username_upper}" ya existe.')
            )
            if Usuario.objects.filter(username=username_upper, is_superuser=True).exists():
                self.stdout.write(
                    self.style.SUCCESS('Ese usuario ya es superusuario de plataforma.')
                )
            return

        rol_admin = Rol.objects.filter(rol='0').first()
        if not rol_admin:
            rol_admin = Rol.objects.filter(id_rol__in=[0, 1]).first()

        try:
            usuario = Usuario.objects.create_user(
                username=username_upper,
                email=email,
                password=password,
            )
            usuario.is_superuser = True
            usuario.id_condominio = None
            if rol_admin:
                usuario.id_rol = rol_admin
            usuario.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSuperusuario de plataforma creado correctamente.\n'
                    f'  Username: {username_upper}\n'
                    f'  Email: {email}\n'
                    f'  id_condominio: (ninguno)\n'
                    f'\nEste usuario debe iniciar sesión desde la pantalla de inicio '
                    f'y será redirigido a la vista de SUPERUSUARIO (cuando esté implementada).'
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al crear superusuario: {e}'))
            raise
