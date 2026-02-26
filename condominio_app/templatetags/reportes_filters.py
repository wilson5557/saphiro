# Filtros y tags para reportes y layout (fecha_deuda, url panel usuario)
from django import template
from django.urls import reverse
from datetime import datetime

register = template.Library()


@register.simple_tag
def url_panel_usuario(user):
    """Enlace del menú: HEADADMIN → superuser; admin (condominio) → home_admin; propietario → home_propietarios."""
    if not user or not getattr(user, 'is_authenticated', False):
        return reverse('condominio_app:home')
    try:
        from condominio_app.models import Usuario
        u = Usuario.objects.select_related('id_rol').filter(pk=user.pk).first()
        if not u:
            return reverse('condominio_app:home')
        if getattr(u, 'is_superuser', False) and getattr(u, 'id_condominio_id', None) is None:
            return reverse('condominio_app:home_superuser')
        rol_val = getattr(getattr(u, 'id_rol', None), 'rol', None)
        if rol_val is not None and str(rol_val) in ('0', '1') and u.id_condominio_id is not None:
            return reverse('condominio_app:home_admin')
        return reverse('condominio_app:home_propietarios')
    except Exception:
        return reverse('condominio_app:home')


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
