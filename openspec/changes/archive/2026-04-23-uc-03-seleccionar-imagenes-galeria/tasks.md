# Tasks: UC-03 Seleccionar imágenes de la galería

## 1. Estado y Persistencia
- [x] 1.1 Refactorizar `_init_session` en `app.py` para incluir `download_queue` (diccionario item_id -> item)
- [x] 1.2 Actualizar `_render_item_card` para que el checkbox lea y escriba en `download_queue`

## 2. UI y Confirmación
- [x] 2.1 Agregar sección "Resumen de Selección" debajo de la galería
- [x] 2.2 Implementar botón "Confirmar Selección" con validación de cola no vacía
- [x] 2.3 Implementar feedback visual (chips o lista) de los IDs seleccionados actualmente

## 3. Integración y Validación
- [x] 3.1 Probar persistencia al realizar una nueva búsqueda con diferentes fechas
- [x] 3.2 Verificar que el estado de selección se mantiene al recargar resultados previos
- [x] 3.3 Validar que el mensaje de "seleccione al menos una imagen" aparece correctamente

## Validation Checklist
- [x] Selección múltiple funcional
- [x] Persistencia entre búsquedas comprobada
- [x] Botón de confirmación operativo
- [x] RF-03 satisfecho
