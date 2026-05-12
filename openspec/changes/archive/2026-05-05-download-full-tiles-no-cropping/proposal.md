## Why

Actualmente, el sistema descarga las bandas de Sentinel-2 aplicando un recorte (cropping) basado en el área de estudio (AOI) proporcionada por el usuario. Sin embargo, para ciertos flujos de trabajo de investigación, es preferible disponer del tile completo (100km x 100km) para asegurar el contexto geográfico total y evitar artefactos de borde en procesamientos posteriores externos.

## What Changes

- **Descarga de Tile Completo**: Se desactivará la lógica de recorte durante la fase de descarga de bandas (`.tif`).
- **Preservación de Metadatos**: Al descargar el tile completo, se mantienen las dimensiones originales y el sistema de referencia de coordenadas intacto sin modificaciones por ventana.
- **Flujo de Procesamiento**: Los pasos posteriores (como la fragmentación en cuadrícula) seguirán funcionando, pero ahora operarán sobre el tile completo descargado en lugar de un recorte parcial.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `UC-04-descargar-bandas-recorte`: Se elimina el requisito de recorte (cropping) durante la descarga, transformando la capacidad en una descarga de tile íntegro.

## Impact

- **src/processor.py**: Modificación de la lógica de descarga para ignorar los límites del AOI al solicitar los datos al STAC API.
- **Almacenamiento**: Incremento significativo en el espacio en disco requerido, ya que cada banda ahora ocupará el tamaño total del tile (~100MB por banda de 10m).
- **Rendimiento**: Los tiempos de descarga aumentarán debido al mayor volumen de datos por archivo.
