# Actualizar el Reporte por Inmueble en otra PC (ej. WorkPC / tutor)

Para que en la PC donde se genera el PDF (por ejemplo la del tutor) se vean **los equivalentes en otra moneda** y las **nuevas secciones** (Relación de gastos por categoría, Movimiento de cuotas y pagos, Movimiento de fondos), hay que tener ahí el código actualizado.

## Archivos que debe tener la otra PC

Copia desde este proyecto (BitBucket/saphiro-condominio) a la misma ruta en la PC del tutor:

1. **`condominio_app/views.py`**  
   - En la parte del reporte `INMUEBLE` debe estar la lógica de `gastos_por_categoria`, movimiento de cuotas/pagos, fondos, y el envío de `tasa_bs` y `tasa_euro` en el contexto.

2. **`templates/PDF/inmueble_pdf.html`**  
   - Debe incluir:
     - Sección "RELACIÓN MENSUAL DE GASTOS (su parte por alícuota)"
     - Sección "MOVIMIENTO DE CUOTAS Y PAGOS DEL PROPIETARIO"
     - Sección "MOVIMIENTO DE FONDOS Y APARTADOS (condominio)"
     - En "DETALLE DE DEUDAS EN EL PERÍODO", columna "Monto (y equivalente)" con el uso de `{% equiv_bcv ... %}` para mostrar el equivalente en la otra moneda.

3. **`condominio_app/templatetags/reportes_filters.py`**  
   - Debe existir el tag `equiv_bcv` y el filtro `format_fecha_deuda` (si ya los tienes en otros reportes, no hace falta cambiar).

## Condición para que se vean los equivalentes (BS ↔ USD)

- En la misma PC donde se genera el reporte debe estar **configurada la tasa BCV** (Configuración → Tasa de cambio). Si la tasa del día no está cargada o es 0, el monto en BS no mostrará equivalente en USD (y al revés). No hace falta cambiar código; solo que la tasa esté guardada y actualizada.

## Después de copiar

1. Reiniciar el servidor Django en la PC del tutor (`python manage.py runserver` o como lo ejecuten).
2. Generar de nuevo el reporte por inmueble (mismo inmueble y rango de fechas) y descargar el PDF.
3. Comprobar que el PDF incluye las tres secciones nuevas y que en la tabla de deudas cada monto muestra, cuando hay tasa, el equivalente (ej. `5 000,00 BS ≈ 11,52 USD`).

Si el PDF sigue igual que antes, revisar que los archivos copiados son los correctos y que no hay otra carpeta del proyecto en uso.
