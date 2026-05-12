## Why

La API STAC de Microsoft Planetary Computer devuelve todos los tiles de Sentinel-2 que intersectan con el AOI de la zona de estudio. Para esta área específica, se retornan 4 tiles por cada toma del satélite: **MPT**, **MPS**, **MQT** y **MQS**. Sin embargo, solo 3 de ellos (**MPS**, **MQT**, **MQS**) son suficientes para cubrir completamente la zona de estudio. El tile **MPT** es redundante y su descarga y procesamiento desperdician tiempo, ancho de banda y almacenamiento.

Esta optimización impacta directamente a RF-01 (Búsqueda Temporal y Espacial) y se propaga a UC-02, UC-03 y UC-04, ya que al reducir la cantidad de items desde la búsqueda, se reducen las previsualizaciones, selecciones y descargas innecesarias.

## What Changes

- Filtrar los items STAC devueltos por la API para **excluir el tile MPT** y conservar únicamente los tiles MPS, MQT y MQS.
- El filtrado se aplicará en el `search_controller.py` después de recibir los resultados de la API STAC, de forma que el resto de la aplicación (galería, descarga, procesamiento) solo vea los 3 tiles relevantes.
- Se añadirá una constante configurable con los tiles permitidos (`ALLOWED_TILES`) para facilitar ajustes futuros si la zona de estudio cambia.
- Se actualizarán los tests unitarios del controlador de búsqueda para verificar el filtrado.

## Capabilities

### New Capabilities
- `tile-filter`: Filtrado de items STAC por tile ID de Sentinel-2, permitiendo restringir los resultados de búsqueda a un subconjunto de tiles que cubren efectivamente la zona de estudio.

### Modified Capabilities
- `UC-01-buscar-imagenes-fecha-area`: El requisito RF-01 se modifica para incluir un paso de filtrado post-búsqueda que descarte tiles innecesarios antes de devolver los resultados al usuario.

## Impact

- **Código afectado**: `src/search_controller.py` (función `search_images` y/o `_parse_item`), tests en `tests/test_search_controller.py`
- **APIs**: Sin cambio en la interfaz pública de `search_images()` — el filtrado es interno y transparente
- **Dependencias**: Ninguna nueva — se usa lógica de filtrado con el `item_id` existente del STAC
- **UC afectados**: UC-01 (directamente), UC-02/UC-03/UC-04 (indirectamente, al recibir menos items)
- **Trazabilidad**: RF-01 → UC-01 → Controlador de Búsqueda (SDD sección 5.1)
