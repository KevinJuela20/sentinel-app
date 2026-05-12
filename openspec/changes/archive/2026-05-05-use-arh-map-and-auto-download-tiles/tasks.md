## 1. Infraestructura y Configuración

- [x] 1.1 Actualizar `DEFAULT_KML_PATH` en `app.py` de `ARH_ETAPA.kml` a `ARH_MAP.kml`.
- [x] 1.2 Actualizar `KML_PATH` en `tests/test_geo_utils.py` para que apunte a `ARH_MAP.kml`.

## 2. Gestión de Archivos y Nomenclatura

- [x] 2.1 Modificar `src/file_manager.py:get_band_filename` para incluir el Tile ID en el nombre del archivo resultante.
- [x] 2.2 Actualizar las llamadas a `get_band_filename` en `src/downloader.py` para pasar el identificador de tile extraído del `item_id`.

## 3. Lógica de Agrupamiento y Búsqueda

- [x] 3.1 Implementar función `group_by_date(items)` en `src/search_controller.py` para agrupar items por fecha `YYYY-MM-DD`.
- [x] 3.2 Asegurar que el filtrado por `ALLOWED_TILES` (`MPS`, `MQT`, `MQS`) siga funcionando correctamente tras el cambio de AOI.

## 4. Rediseño de la Interfaz de Usuario (Streamlit)

- [x] 4.1 Actualizar la inicialización del estado de sesión en `app.py` para manejar una cola de descarga estructurada por fecha.
- [x] 4.2 Modificar `_render_results` para iterar sobre grupos de fechas en lugar de una lista plana de items.
- [x] 4.3 Implementar `_render_date_card` para mostrar una previsualización por fecha y permitir la selección masiva de sus tiles.
- [x] 4.4 Actualizar el resumen de la cola de descarga para reflejar las fechas seleccionadas y el número total de tiles.

## 5. Orquestación de Descarga Automática

- [x] 5.1 Modificar `_run_download_process` en `app.py` para iterar sobre todos los tiles de cada fecha seleccionada.
- [x] 5.2 Ajustar la barra de progreso para reflejar el avance total (Tiles * Bandas) de la descarga.

## 6. Verificación y Pruebas

- [x] 6.1 Ejecutar tests unitarios de `geo_utils` y `file_manager`.
- [x] 6.2 Realizar prueba de integración manual: buscar imágenes con el nuevo AOI, seleccionar una fecha y verificar que se descarguen los 3 tiles en la carpeta correspondiente con nombres correctos.
