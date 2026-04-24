# Tasks: UC-05 Procesar recortes y filtrar nubes

## 1. Motores de Procesamiento (Infrastructure)
- [x] 1.1 Crear `sentinel-project/src/processor.py` para la iteración sobre la cuadrícula
- [x] 1.2 Implementar lógica de filtrado SCL (umbral 5%) en `processor.py`
- [x] 1.3 Crear `sentinel-project/src/image_utils.py` para la composición RGB y conversión a 8-bit PNG

## 2. Orquestación y Limpieza (Application)
- [x] 2.1 Implementar `process_all_grids(date_path, grid_path)`:
  - Cargar GeoJSON
  - Iterar y aplicar filtro/recorte
  - Guardar en subcarpeta `crops/`
- [x] 2.2 Implementar lógica de limpieza de archivos `.tif` temporales tras éxito

## 3. Integración UI (Presentation)
- [x] 3.1 Agregar pestaña o botón "Generar Recortes (IA Ready)" en `app.py`
- [x] 3.2 Mostrar log en tiempo real de polígonos aceptados vs descartados
- [x] 3.3 Mostrar resumen de espacio liberado tras la limpieza

## 4. Pruebas (Environment Local)
- [x] 4.1 Escribir unit tests para el filtro SCL (usando `python3 -m pytest`)
- [x] 4.2 Escribir unit tests para la composición RGB
- [x] 4.3 **IMPORTANTE**: No usar `conda run` para las pruebas; usar el entorno de sistema `python3`

## Validation Checklist
- [x] Recortes generados solo para áreas limpias (SCL < 5% nubes)
- [x] Formato de salida PNG RGB 8-bit correcto
- [x] Archivos .tif eliminados automáticamente tras proceso
- [x] RF-05 y RF-07 satisfechos
