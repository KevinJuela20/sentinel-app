## 1. Ajustes en Utilidades de Imagen

- [x] 1.1 Modificar `src/image_utils.py:save_rgb_png` para incluir un paso de redimensionamiento a 128x128 píxeles usando `PIL.Image.LANCZOS` o `Resampling.LANCZOS`.

## 2. Refactorización del Procesador Multi-tile

- [x] 2.1 Actualizar `src/processor.py:process_all_grids` para descubrir Tile IDs en el directorio y agrupar bandas correctamente.
- [x] 2.2 Modificar `src/processor.py:process_all_grids` para iterar sobre cada grupo de tiles de forma independiente.
- [x] 2.3 Ajustar la lógica de nombrado en `src/processor.py` para incluir el Tile ID en el nombre del recorte PNG resultante.

## 3. Validación de Dimensiones y Recorte

- [x] 3.1 Implementar validación de tamaño ($\ge 124 \times 124$) en `src/processor.py:process_grid_cell` justo después de la máscara del raster.
- [x] 3.2 Asegurar que los recortes descartados por tamaño sean registrados en el log para trazabilidad.

## 4. Integración en la Interfaz de Usuario

- [x] 4.1 Verificar la integración en `app.py` para asegurar que el disparador del procesador maneje correctamente el flujo multi-tile (si se requiere algún cambio en la llamada).

## 5. Verificación y Pruebas

- [x] 5.1 Crear script de prueba para verificar la validación de 124x124 con un raster de prueba pequeño.
- [x] 5.2 Realizar prueba de integración manual: procesar una fecha con 3 tiles y verificar que la carpeta `crops/` contenga recortes de todos los tiles, todos de tamaño 128x128.
- [x] 5.3 Validar que el proceso de Súper-Resolución procese todos los archivos `_SR.png` generados.
