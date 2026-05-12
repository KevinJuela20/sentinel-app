## 1. Actualización de Configuración

- [x] 1.1 Modificar `DEFAULT_BANDS` en `src/file_manager.py` eliminando el elemento `"visual"`.
- [x] 1.2 Verificar que `app.py` no asuma la existencia de la banda `"visual"` en la inicialización de progreso o conteo.

## 2. Refactorización del Procesador (Mosaico)

- [x] 2.1 Localizar la lógica de generación de mosaico (`rasterio.merge` o `create_mosaic`) en `src/processor.py` (función `process_all_grids`).
- [x] 2.2 Modificar la recolección de `visual_paths` para que no falle si la banda `"visual"` no se encuentra en `tiles_data`.
- [x] 2.3 Implementar la lógica alternativa: si se requiere el mosaico, generarlo a partir de las bandas B04, B03 y B02 apiladas (stack), o bien, omitir la generación del mosaico de referencia de forma segura e informar al usuario.

## 3. Verificación

- [x] 3.1 Realizar una descarga de prueba y confirmar que solo se descargan las bandas B02, B03, B04 y SCL.
- [x] 3.2 Verificar que el proceso posterior de generación de recortes (`process_all_grids`) se ejecuta correctamente sin la banda `visual`.
