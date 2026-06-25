## Why

Al procesar los recortes de la cuadrícula, la zona de estudio abarca tres TILES de Sentinel-2 (MPS, MQT, MQS) que se superponen parcialmente. El bucle actual itera cada tile sobre **todas** las celdas de la cuadrícula, lo que genera recortes duplicados para las celdas ubicadas en zonas de solapamiento. Esto causa almacenamiento innecesario, redimensionamientos redundantes que consumen recursos y, potencialmente, imágenes duplicadas que afectan el entrenamiento de modelos de IA. Se requiere una validación de deduplicación en el proceso de recorte (RF-05 / UC-05).

## What Changes

- **Agregar un diccionario de asignación fija de IDs de borde a tiles específicos** (`IDS_POR_TILE`). Los IDs que se encuentran en los bordes entre tiles solo se recortarán desde el tile asignado, evitando recortes parciales o de menor calidad.
- **Agregar validación de existencia previa del recorte**. Para los IDs que NO están en la lista de borde, antes de recortar se verifica si ya existe un PNG guardado con ese `cell_id` y `date_str`. Si ya existe, se omite el recorte del tile actual.
- **Mantener la validación SCL/nubes existente** como paso posterior. Un recorte solo se guarda si pasa tanto la validación de deduplicación como la de nubes.
- **Sin cambios en la estructura de archivos de salida** ni en la interfaz de usuario. El cambio es puramente en la lógica interna de `processor.py`.

## Capabilities

### New Capabilities
- `tile-dedup-filter`: Lógica de deduplicación de recortes por ID de celda. Incluye la asignación fija de IDs de borde a tiles y la verificación de existencia previa en disco para IDs no asignados.

### Modified Capabilities
- `UC-05-procesar-recortes-filtrar-nubes`: Se agrega un paso previo de deduplicación antes del filtrado de nubes. La especificación del escenario "Procesamiento de múltiples tiles por fecha" se enriquece con la lógica de asignación de tile preferente y verificación de existencia previa.

## Impact

- **Código afectado**: `sentinel-project/src/processor.py` — funciones `process_all_grids` y `process_grid_cell`.
- **Sin cambios en APIs externas**: la firma de `process_all_grids` no cambia.
- **Sin nuevas dependencias**: se usa solo `pathlib.Path.glob()` para verificar existencia en disco.
- **Trazabilidad**: RF-05, UC-05 (Motor de Procesamiento + Filtro de Nubes).
