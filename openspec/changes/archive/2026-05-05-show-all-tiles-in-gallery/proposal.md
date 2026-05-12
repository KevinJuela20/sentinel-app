## Why

Actualmente, el sistema agrupa los resultados por fecha pero solo muestra la previsualización de uno de los tres tiles (MPS, MQT o MQS) asociados a esa fecha. Para asegurar que la zona de estudio completa esté libre de nubes y correctamente capturada, el usuario necesita visualizar los tres tiles antes de proceder con la descarga.

## What Changes

- **Galería Multi-Tile**: La interfaz se rediseñará para mostrar los tres tiles de forma individual dentro de cada grupo de fecha.
- **Pre-carga Paralela**: Se optimizará el cargador de previsualizaciones para procesar los tres assets por fecha simultáneamente.
- **Control de Selección**: Se mantendrá la selección por fecha única (que incluye los 3 tiles), pero con una visualización clara de cada componente.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `UC-02-previsualizacion-mascara-aoi`: Se actualiza el requisito de visualización para soportar la renderización de múltiples tiles por grupo de fecha en la galería de resultados.

## Impact

- **app.py**: Refactorización de `_render_date_card` a un formato de sección multi-columna.
- **src/preview_engine.py**: Asegurar que las llamadas concurrentes manejen correctamente el volumen de imágenes (3x por fecha).
- **Interfaz de Usuario**: Cambio en la disposición de la galería de 3 columnas fijas a una estructura de filas por fecha con sub-columnas para tiles.
