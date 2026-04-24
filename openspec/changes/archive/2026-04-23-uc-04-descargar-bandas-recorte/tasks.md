# Tasks: UC-04 Descargar bandas y recorte

## 1. Motores de Base (Infrastructure)
- [x] 1.1 Crear `sentinel-project/src/file_manager.py` para la gestión jerárquica de carpetas
- [x] 1.2 Implementar lógica de firma de URLs en `sentinel-project/src/downloader.py`
- [x] 1.3 Implementar lógica de recorte (clip) con `rasterio` en `downloader.py`

## 2. Lógica de Descarga (Application)
- [x] 2.1 Implementar `download_bands(item, target_dir, geojson_geom)`:
  - Firmar B02, B03, B04, SCL, Visual
  - Aplicar máscara y guardar TIF
- [x] 2.2 Implementar manejo de errores y reintentos básicos

## 3. Integración UI (Presentation)
- [x] 3.1 Agregar sección de "Descarga" en `app.py` (aparece tras confirmar selección)
- [x] 3.2 Implementar barra de progreso dinámica
- [x] 3.3 Notificación final de "Descarga Completada" con resumen de archivos

## 4. Pruebas
- [x] 4.1 Escribir unit tests para `file_manager.py` (creación de rutas)
- [x] 4.2 Escribir unit tests para `downloader.py` (mock de rasterio/mask)
- [x] 4.3 Validación manual de los archivos TIF generados (abrir en GIS si es posible)

## Validation Checklist
- [x] Bandas descargadas y recortadas correctamente
- [x] Estructura `Data_Sentinel/[Año]/[Mes]/[Día]` creada
- [x] Barra de progreso funcional
- [x] RF-04 y RF-07 satisfechos
