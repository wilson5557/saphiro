"""
Comando para inicializar todos los roles del sistema
Uso: python manage.py init_roles

Este comando crea los roles necesarios si no existen.
IMPORTANTE: Los roles se identifican por el campo 'rol' (valores '0', '1', '2', etc.),
NO por el id_rol que es AutoField. El código debe usar el campo 'rol' para las comparaciones.
"""
from django.core.management.base import BaseCommand
from condominio_app.models import Rol


class Command(BaseCommand):
    help = 'Inicializa todos los roles del sistema (Administrador, Presidente, Secretario, Junta, Propietario, Portero)'

    def handle(self, *args, **options):
        # Definir los roles según el modelo (el valor del choice)
        roles_data = [
            ('0', 'Administrador'),
            ('1', 'Presidente'),
            ('2', 'Secretario/a'),
            ('3', 'Junta'),
            ('4', 'Propietario'),
            ('5', 'Portero'),
        ]
        
        created_count = 0
        existing_count = 0
        
        for rol_value, rol_name in roles_data:
            # Verificar si el rol ya existe por su valor
            rol_existente = Rol.objects.filter(rol=rol_value).first()
            
            if not rol_existente:
                # Crear el rol
                Rol.objects.create(rol=rol_value)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Rol creado: {rol_name}')
                )
                created_count += 1
            else:
                existing_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Proceso completado!\n'
                f'   Roles creados: {created_count}\n'
                f'   Roles existentes: {existing_count}\n'
                f'   Total de roles: {Rol.objects.count()}'
            )
        )
