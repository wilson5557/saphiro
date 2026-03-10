# Filtros y tags para reportes y layout (fecha_deuda, url panel usuario)
from django import template
from django.urls import reverse
from datetime import datetime
from decimal import Decimal

register = template.Library()


@register.simple_tag
def equiv_bcv(monto, tipo_moneda, tasa_bs, tasa_euro):
    """
    Devuelve el equivalente del monto en la otra moneda (BCV).
    - BS -> equivalente en USD (monto/tasa_bs)
    - USD -> equivalente en BS (monto*tasa_bs)
    - EUR -> equivalente en BS (monto*tasa_euro)
    Retorna dict con 'value' y 'currency' o None si no hay tasa.
    """
    if monto is None:
        return None
    try:
        m = Decimal(str(monto))
    except (TypeError, ValueError):
        return None
    moneda = (tipo_moneda or '').strip().upper() or 'BS'
    try:
        t_bs = Decimal(str(tasa_bs or 0))
        t_eur = Decimal(str(tasa_euro or 0))
    except (TypeError, ValueError):
        return None
    if moneda == 'BS':
        if t_bs and t_bs > 0:
            return {'value': (m / t_bs).quantize(Decimal('0.01')), 'currency': 'USD'}
        return None
    if moneda == 'USD':
        if t_bs and t_bs > 0:
            return {'value': (m * t_bs).quantize(Decimal('0.01')), 'currency': 'BS'}
        return None
    if moneda == 'EUR':
        if t_eur and t_eur > 0:
            return {'value': (m * t_eur).quantize(Decimal('0.01')), 'currency': 'BS'}
        return None
    return None


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
def formato_moneda(value):
    """Formato de monto con signo menos al inicio si es negativo (evita '123,45-'). Usar en PDFs."""
    if value is None:
        return '—'
    try:
        m = Decimal(str(value))
    except (TypeError, ValueError):
        return str(value)
    from django.contrib.humanize import intcomma
    q = abs(m).quantize(Decimal('0.01'))
    signo = '- ' if m < 0 else ''
    return signo + intcomma(float(q))


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
