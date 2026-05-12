## Why

Actualmente, el sistema descarga el asset `visual` (True Color) de Sentinel-2 además de las bandas individuales B04 (Rojo), B03 (Verde) y B02 (Azul). Dado que el producto visual puede reconstruirse localmente a partir de las bandas individuales, su descarga representa una redundancia de datos innecesaria que consume ancho de banda y espacio en disco.

## What Changes

- **Eliminación de Descarga Redundante**: Se eliminará el asset `visual` de la lista de bandas a descargar por defecto.
- **Optimización de Almacenamiento**: Reducción del volumen de datos descargados por tile en aproximadamente un 20%.
- **Reconstrucción Local**: Los procesos que dependan de una imagen visual (como la generación del mosaico de referencia) deberán utilizar las bandas B04, B03 y B02 descargadas.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `UC-04-descargar-bandas-recorte`: Se actualiza la lista de assets requeridos para excluir el producto `visual` pre-procesado por MPC.

## Impact

- **src/file_manager.py**: Actualización de la constante `DEFAULT_BANDS`.
- **src/processor.py**: Modificación de la lógica de generación del mosaico para que utilice las bandas RGB locales en lugar de buscar un archivo `visual.tif`.
- **Ancho de Banda**: Reducción en el tiempo de descarga total al omitir un asset pesado.
