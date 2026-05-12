## 1. Utilidades de Mosaico

- [x] 1.1 Implementar la función `create_mosaic(input_paths, output_path)` en `src/image_utils.py` utilizando `rasterio.merge`.

## 2. Orquestación en el Procesador

- [x] 2.1 Modificar `src/processor.py:process_all_grids` para recolectar las rutas de los archivos `*_visual.tif` de todos los tiles disponibles.
- [x] 2.2 Integrar la llamada a `create_mosaic` en `process_all_grids` justo antes de la sección de limpieza de archivos temporales.
- [x] 2.3 Asegurar que el nombre del archivo resultante siga el patrón `Color_YYYY-MM-DD.tif`.

## 3. Verificación

- [x] 3.1 Realizar prueba de integración manual: procesar una fecha y verificar la existencia del archivo `Color_*.tif` con la imagen unificada de la zona de estudio.
