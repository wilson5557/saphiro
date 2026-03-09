# Diagnóstico y revisión – saphiro-condominio

**Fecha:** Revisión realizada para evitar fallos por `ultima_tasa` None y flujos críticos.

---

## 1. Django check

- **Resultado:** `System check identified no issues (0 silenced).`
- **Comando:** `python manage.py check`

---

## 2. Cambios realizados (protección ante fallos)

### 2.1 Función auxiliar `_obtener_tasas_safe`

- **Ubicación:** `condominio_app/views.py` (después de `actualizar_tasa`).
- **Uso:** Devuelve `(tasa_bs, tasa_euro)`. Si `ultima_tasa` es `None`, devuelve `(0, 0)` y no se llama a `comprobar_tasa`, evitando `AttributeError`.
- **Vistas que la usan:** Todas las que antes hacían `tasa_bs = ultima_tasa.tasa_BCV_USD` y `comprobar_tasa` sin comprobar si `ultima_tasa` era `None`.

### 2.2 Vistas que ya no fallan sin tasas en BD

- **Propietarios (pagos):** usa `_obtener_tasas_safe`; si no hay tasas se usan 0, 0.
- **Admin configuración (recargos/descuentos, precios, etc.):** usan `_obtener_tasas_safe`.
- **Configuración tasas de cambio:** ya manejaba `ultima_tasa is None` (crear primera tasa y formulario).
- **Otras vistas (gastos, ingresos, fondos, bancos, etc.):** o bien redirigen a “Configurar tasas” cuando no hay `ultima_tasa`, o bien usan `_obtener_tasas_safe`.

### 2.3 Tarea Celery `comprobar_tasa` (tasks.py)

- Si no hay ninguna tasa en BD, la tarea hace `return` al inicio y no accede a `ultima_tasa.updated_at` ni a `tasa_BCV_*`, evitando fallos.

### 2.4 Formulario de bancos (admin_bancos)

- Conversión de `fecha_apertura` (un solo campo desde Configuración) a día/mes/año para que el formulario valide.
- Se mantiene `bancos_form.save()` (commit=True) para que se cree correctamente el movimiento de apertura.
- Mensaje de error del formulario incluye el detalle de los primeros errores de validación.

---

## 3. Puntos que siguen requiriendo tasas

- **Configuración (excepto Tasas):** Si no hay tasas, se redirige a Configuración → Tasas antes de usar otros módulos.
- **Gastos, ingresos, fondos, deudas, cierres, etc.:** Si no hay tasas, se redirige a configurar tasas. No se permite usar esos módulos sin al menos una tasa.

---

## 4. Cómo volver a diagnosticar

En la raíz del proyecto:

```bash
python manage.py check
```

Para comprobar imports y que las vistas carguen:

```bash
python manage.py shell -c "from condominio_app.views import _obtener_tasas_safe, actualizar_tasa; print('OK')"
```

---

## 5. Resumen

- **Nada debería fallar** por `ultima_tasa` en `None`: o se usa `_obtener_tasas_safe` (0, 0) o se redirige a Configuración → Tasas.
- **Bancos:** El flujo de alta de bancos desde Configuración es compatible con el formulario (fecha y validación).
- **Tasas:** La primera tasa se puede crear desde Configuración → Tasas aunque no exista aún ningún registro en la tabla Tasas.
