## Why

Este cambio habilita la capacidad crítica de obtener datos satelitales en alta resolución (bandas 10m y 20m) procesados específicamente para el área de estudio. El recorte automático a la cuadrícula del proyecto (`Cuadrícula_ARH.geojson`) y la organización jerárquica por fechas son fundamentales para que los analistas puedan integrar los datos directamente en sus flujos GIS sin procesamiento manual adicional.

## What Changes

- **Motor de Descarga (DownloaderEngine)**: Implementación de la lógica para firmar URLs de Microsoft Planetary Computer y descargar assets de forma asíncrona o secuencial con manejo de errores.
- **Procesamiento Geoespacial (Clipping)**: Aplicación de máscaras espaciales mediante `rasterio` utilizando la geometría detallada de `Cuadrícula_ARH.geojson`.
- **Gestor de Archivos (FileManager)**: Creación automatizada de la estructura de directorios `Data_Sentinel/[Año]/[Mes]/[Día]` y estandarización de nombres de archivos.
- **Interfaz de Usuario**: Barra de progreso detallada y registro de estado de descarga en Streamlit para informar al usuario sobre el avance de las tareas pesadas.

## Capabilities

### New Capabilities
- Ninguna (implementación de capacidad base definida en UC-04).

### Modified Capabilities
- `uc-04-descargar-bandas-recorte`: Implementación de los requisitos funcionales RF-04 y RF-07 detallados en el baseline spec.

## Impact

- **sentinel-project/src/downloader.py**: Nuevo módulo para la lógica de descarga y firma.
- **sentinel-project/src/file_manager.py**: Nuevo módulo para la gestión de carpetas y nombres.
- **sentinel-project/app.py**: Integración de la sección de descarga y control de progreso.
- **Almacenamiento**: Se requerirá espacio en disco para los archivos TIF (aprox. 100-200MB por imagen seleccionada).
