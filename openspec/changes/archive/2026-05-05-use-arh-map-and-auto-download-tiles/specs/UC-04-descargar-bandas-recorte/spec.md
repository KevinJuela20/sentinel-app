## MODIFIED Requirements

### Requirement: Descarga Optimizada de Bandas Seleccionadas (RF-04)
El sistema SHALL descargar las bandas B02, B03, B04 y SCL, además del producto True Color (.tif) para **cada uno de los tiles** asociados a las fechas seleccionadas. El sistema SHALL realizar un recorte (clip) a los polígonos del archivo `Cuadrícula_ARH.geojson` para cada tile descargado. Los archivos resultantes deben ser GeoTIFF con el CRS correcto y almacenarse en la misma carpeta de fecha, diferenciados por el ID del tile.

#### Scenario: Descarga automática de los tres tiles por fecha
- **WHEN** el usuario inicia el proceso de descarga para una fecha seleccionada
- **THEN** el sistema identifica todos los items (tiles) asociados a esa fecha en la cola de descarga
- **AND** para cada item, firma las URLs de los assets: B02, B03, B04, SCL y Visual
- **AND** descarga y recorta cada banda usando `Cuadrícula_ARH.geojson`
- **AND** guarda los archivos en `Data_Sentinel/[Año]/[Mes]/[Día]/`
- **AND** los nombres de archivo incluyen el Tile ID para evitar colisiones (ej: `20250101_MPS_B02.tif`)
- **AND** la barra de progreso refleja el avance total de todos los tiles y bandas de la fecha
