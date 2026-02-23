# Filtros para reportes PDF (fecha_deuda es CharField, no DateField)
from django import template
from datetime import datetime

register = template.Library()


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
