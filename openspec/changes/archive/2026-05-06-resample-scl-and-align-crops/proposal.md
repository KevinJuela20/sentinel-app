## Why

Actualmente, el sistema realiza recortes independientes para cada banda (SCL a 20m, RGB a 10m) usando `rasterio.mask`, lo que puede generar ligeros desajustes en las dimensiones finales y la alineación de píxeles entre bandas de distinta resolución nativa. Para garantizar la consistencia espacial requerida en el entrenamiento de modelos de IA, es necesario alinear todas las extracciones a la resolución de referencia de 10m (Banda B04).

## What Changes

- **Alineación Espacial con B04**: Se utilizará la banda B04 (10m) como referencia para definir la ventana (`window`) de extracción de todas las demás bandas.
- **Resampling de SCL a 10m**: La capa SCL será re-mureada (resampled) a 10 metros mediante interpolación bilineal durante la lectura, permitiendo una correspondencia exacta de píxeles con el producto RGB.
- **Validación Dual de Nubes**: Se mantiene la validación de nubes en la resolución nativa de 20m para mayor precisión en el filtrado, pero la extracción final se realiza en la cuadrícula de 10m.
- **Preservación de Tamaño de Salida**: Se garantiza que todos los recortes tengan el tamaño exacto definido (ej. 128x128 píxeles si la celda lo permite), descartando fragmentos incompletos menores a 63 píxeles (según ajuste reciente del usuario).

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `UC-05-procesar-recortes-filtrar-nubes`: Se actualiza el requisito de procesamiento para incluir el re-muestreo de la capa SCL a 10m y el uso de ventanas de referencia basadas en la banda B04.

## Impact

- **src/processor.py**: Modificación de `process_grid_cell` para implementar el flujo de: Transformación → Ventana en B04 → Validación SCL 20m → Lectura con Resampling a 10m.
- **src/image_utils.py**: Posible actualización en la normalización si se requieren ajustes de contraste específicos mencionados en el código de referencia.
- **Rendimiento**: Ligero incremento en el tiempo de procesamiento debido a la interpolación bilineal al vuelo durante la lectura.
