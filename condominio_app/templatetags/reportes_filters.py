# Filtros y tags para reportes y layout (fecha_deuda, url panel usuario)
from django import template
from django.urls import reverse
from datetime import datetime

register = template.Library()


@register.simple_tag
def url_panel_usuario(user):
    """Enlace del menú: con condominio → /home/administrador/; HEADADMIN (sin condominio + superuser) → superuser; resto → propietarios."""
    if not user or not getattr(user, 'is_authenticated', False):
        return reverse('condominio_app:home')
    try:
        from condominio_app.models import Usuario
        # Una sola consulta mínima: solo condominio y superuser (evita errores de rol)
        row = Usuario.objects.filter(pk=user.pk).values('id_condominio_id', 'is_superuser').first()
        if not row:
            return reverse('condominio_app:home_propietarios')
        # Quien tiene condominio es ADMIN de condominio → siempre panel admin (no propietarios)
        if row.get('id_condominio_id') is not None:
            return reverse('condominio_app:home_admin')
        if row.get('is_superuser'):
            return reverse('condominio_app:home_superuser')
        # Sin condominio y no superuser: puede ser admin sin asignar o propietario; envía a admin por defecto si hay duda
        return reverse('condominio_app:home_propietarios')
    except Exception:
        return reverse('condominio_app:home_propietarios')


@register.filter
def format_fecha_deuda(value):
    """Formatea string YYYY-MM-DD a dd/mm/yyyy. Si está vacío o no es esa forma, devuelve el valor o '—'."""
    if value is None or str(value).strip() == '':
        return '—'
    s = str(value).strip()
    try:
        dt = datetime.strptime(s[:10], '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        return s if s else '—'
