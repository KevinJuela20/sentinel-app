## 1. Identificación y Modificación del Núcleo de Descarga

- [x] 1.1 Localizar la función `_download_asset` o equivalente en `src/processor.py` que realiza el recorte con el AOI.
- [x] 1.2 Implementar una nueva lógica de descarga directa utilizando `requests` o el método nativo de `pystac` para guardar el archivo completo en disco sin procesar.
- [x] 1.3 Desvincular el parámetro `aoi_geom` del proceso de guardado de bandas `.tif`.

## 2. Refactorización del Flujo de Datos

- [x] 2.1 Asegurar que la función `_run_download_process` en `app.py` siga reportando el progreso correctamente a pesar del mayor tamaño de los archivos.
- [x] 2.2 Verificar que el paso de limpieza de temporales no se vea afectado por el cambio en el tamaño de los archivos base.
- [x] 2.3 Validar que el paso posterior de fragmentación (UC-05) maneje correctamente los archivos `.tif` completos como entrada.

## 3. Verificación

- [x] 3.1 Realizar una descarga de prueba y confirmar mediante `rio info` o similar que las dimensiones del archivo corresponden al tile original de Sentinel-2 (ej. 10980x10980).
- [x] 3.2 Verificar físicamente que los archivos `.tif` descargados cubren un área mucho mayor que el AOI original.
