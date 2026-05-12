## Why

Se requiere actualizar la zona de estudio para cubrir un área más amplia y simplificar el flujo de descarga. Actualmente, el usuario debe seleccionar manualmente los tiles (sub-áreas) de interés, lo cual es ineficiente ya que el proyecto siempre requiere la cobertura total de la nueva zona de estudio (ARH_MAP) en cada fecha procesada. Al automatizar la descarga de los tres tiles correspondientes a cada fecha, se reduce el error humano y se agiliza la preparación de datos para los procesos de IA posteriores.

## What Changes

- **Cambio de AOI por defecto**: Se sustituye el archivo `ARH_ETAPA.kml` por `ARH_MAP.kml` como la geometría de referencia para búsquedas y recortes.
- **Selección por Fecha**: Se modifica la interfaz de selección de imágenes para que el usuario seleccione "Fechas" en lugar de "Tiles" individuales.
- **Descarga Automática de Tiles**: Al confirmar una fecha, el sistema descargará automáticamente los tres tiles permitidos (`MPS`, `MQT`, `MQS`) disponibles para esa fecha.
- **Simplificación de la Galería**: La galería mostrará una representación única por fecha (o agrupará los tiles) para reflejar que la unidad de selección es el día de adquisición.

## Capabilities

### New Capabilities
- Ninguna. Se trata de una evolución de las capacidades existentes.

### Modified Capabilities
- `UC-01-buscar-imagenes-fecha-area`: El área de interés por defecto cambia a `ARH_MAP.kml`.
- `UC-03-seleccionar-imagenes-galeria`: La unidad de selección cambia de "Item STAC (Tile)" a "Fecha de Adquisición (Grupo de Tiles)". **BREAKING**
- `UC-04-descargar-bandas-recorte`: El proceso de descarga ahora itera sobre todos los tiles disponibles para una fecha seleccionada en lugar de un solo item.

## Impact

- **Frontend (`app.py`)**: Cambios significativos en la lógica de `render_results`, `render_item_card` y la gestión del `download_queue`.
- **Controlador (`search_controller.py`)**: Posible necesidad de agrupar resultados por fecha antes de retornarlos a la UI.
- **Configuración**: Actualización de la ruta de KML por defecto.
- **Pruebas**: Se deben actualizar los tests de integración que dependían de la selección individual de tiles.
