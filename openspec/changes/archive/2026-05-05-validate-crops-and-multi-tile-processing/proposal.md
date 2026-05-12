## Why

El sistema de descarga de Sentinel-2 ahora soporta la descarga de múltiples tiles por fecha (MPS, MQT, MQS). Sin embargo, el motor de fragmentación actual no está optimizado para procesar varios tiles simultáneamente y genera recortes incompletos o con artefactos en los bordes de los tiles que degradan la calidad del entrenamiento de los modelos de IA. Es necesario implementar una validación de dimensiones mínimas y una normalización de tamaño (128x128) para asegurar que solo datos de alta calidad lleguen al pipeline de súper-resolución.

## What Changes

- **Validación de Dimensiones**: Se agrega un filtro en el procesamiento de celdas para descartar recortes con dimensiones menores a 124x124 píxeles (recortes de borde).
- **Redimensionamiento Estándar**: Todos los recortes que superen la validación serán redimensionados a exactamente 128x128 píxeles.
- **Soporte Multi-tile en Procesamiento**: La fragmentación y la súper-resolución ahora iterarán sobre todos los tiles descargados para una fecha específica, asegurando la cobertura total del área de estudio.
- **Pipeline de Súper-Resolución**: Se formaliza el escalado de 128x128 a 1024x1024 píxeles usando los modelos EDSR existentes.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `UC-05-procesar-cuadricula-nubes`: Se añade la validación de dimensiones de recorte (min 124x124) y el redimensionamiento a 128x128 antes de guardar el PNG. Se añade el soporte para iterar sobre múltiples tiles.
- `UC-06-aumento-resolucion-ia`: Se ajusta para procesar el lote completo de recortes generados a partir de múltiples tiles.

## Impact

- **src/processor.py**: Cambio en la lógica de `process_all_grids` para agrupar por Tile ID y en `process_grid_cell` para validar dimensiones.
- **src/image_utils.py**: Nueva utilidad o ajuste en `save_rgb_png` para incluir el redimensionamiento a 128x128.
- **src/super_resolution.py**: Verificación de que el batch processing maneje correctamente los nuevos nombres de archivo con ID de Tile.
- **app.py**: Actualización de la llamada al procesador para manejar el flujo multi-tile.
